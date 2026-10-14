// Re-encodes a video with a lower bitrate using macOS's own framework (no ffmpeg needed). Runs locally, no API call, original untouched.
// Usage: swift tools/compress_video.swift INPUT.mp4 OUTPUT.mp4 [VIDEO_KBPS=1300] [AUDIO_KBPS=96]
import AVFoundation
import Foundation

let args = CommandLine.arguments
guard args.count >= 3 else { print("Usage: compress_video.swift IN OUT [video_kbps] [audio_kbps]"); exit(2) }
let vk = args.count > 3 ? Int(args[3]) ?? 1300 : 1300
let ak = args.count > 4 ? Int(args[4]) ?? 96 : 96
let src = AVURLAsset(url: URL(fileURLWithPath: args[1]))
let out = URL(fileURLWithPath: args[2]); try? FileManager.default.removeItem(at: out)
let reader = try! AVAssetReader(asset: src)
let writer = try! AVAssetWriter(outputURL: out, fileType: .mp4)
let vt = src.tracks(withMediaType: .video)[0]
let vOut = AVAssetReaderTrackOutput(track: vt, outputSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_420YpCbCr8BiPlanarVideoRange])
reader.add(vOut)
let size = vt.naturalSize
let vIn = AVAssetWriterInput(mediaType: .video, outputSettings: [
  AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: Int(size.width), AVVideoHeightKey: Int(size.height),
  AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: vk * 1000, AVVideoMaxKeyFrameIntervalKey: 48, AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel, AVVideoExpectedSourceFrameRateKey: 24]])
vIn.transform = vt.preferredTransform; vIn.expectsMediaDataInRealTime = false; writer.add(vIn)
var aOut: AVAssetReaderTrackOutput? = nil; var aIn: AVAssetWriterInput? = nil
if let at = src.tracks(withMediaType: .audio).first {
  // keep the source channel layout (mono stays mono): forcing stereo on a mono source made it about 3 dB louder
  var ch = 2
  if let fd = at.formatDescriptions.first, let asbd = CMAudioFormatDescriptionGetStreamBasicDescription(fd as! CMAudioFormatDescription) { ch = Int(asbd.pointee.mChannelsPerFrame) }
  aOut = AVAssetReaderTrackOutput(track: at, outputSettings: [AVFormatIDKey: kAudioFormatLinearPCM, AVLinearPCMBitDepthKey: 16, AVLinearPCMIsFloatKey: false, AVLinearPCMIsBigEndianKey: false, AVLinearPCMIsNonInterleaved: false, AVSampleRateKey: 44100, AVNumberOfChannelsKey: ch])
  reader.add(aOut!)
  aIn = AVAssetWriterInput(mediaType: .audio, outputSettings: [AVFormatIDKey: kAudioFormatMPEG4AAC, AVSampleRateKey: 44100, AVNumberOfChannelsKey: ch, AVEncoderBitRateKey: ak * (ch == 1 ? 700 : 1000)])
  aIn!.expectsMediaDataInRealTime = false; writer.add(aIn!)
}
reader.startReading(); writer.startWriting(); writer.startSession(atSourceTime: .zero)
let group = DispatchGroup()
func pump(_ input: AVAssetWriterInput, _ output: AVAssetReaderTrackOutput, _ q: String) {
  group.enter()
  input.requestMediaDataWhenReady(on: DispatchQueue(label: q)) {
    while input.isReadyForMoreMediaData {
      if let s = output.copyNextSampleBuffer() { input.append(s) } else { input.markAsFinished(); group.leave(); break }
    }
  }
}
pump(vIn, vOut, "v"); if let ai = aIn, let ao = aOut { pump(ai, ao, "a") }
group.wait()
writer.finishWriting { }
while writer.status == .writing { Thread.sleep(forTimeInterval: 0.1) }
print("status", writer.status.rawValue, writer.error?.localizedDescription ?? "")

// Copies a video and repeats its last frame N extra times at 24 fps (constant frame rate, H.264).
// Called by hold_last_frame.sh. Usage: swift hold_last_frame.swift SRC DST EXTRA_FRAMES
import AVFoundation
let src = URL(fileURLWithPath: CommandLine.arguments[1])
let dst = URL(fileURLWithPath: CommandLine.arguments[2])
let extraFrames = Int(CommandLine.arguments[3])!
let asset = AVURLAsset(url: src)
let track = asset.tracks(withMediaType: .video)[0]
let size = track.naturalSize
let fps: Int32 = 24
let reader = try! AVAssetReader(asset: asset)
let out = AVAssetReaderTrackOutput(track: track, outputSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA])
reader.add(out)
let writer = try! AVAssetWriter(outputURL: dst, fileType: .mp4)
let input = AVAssetWriterInput(mediaType: .video, outputSettings: [
  AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: Int(size.width), AVVideoHeightKey: Int(size.height),
  AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: 8_000_000, AVVideoExpectedSourceFrameRateKey: 24]])
input.expectsMediaDataInRealTime = false
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: input, sourcePixelBufferAttributes: nil)
writer.add(input)
reader.startReading(); writer.startWriting(); writer.startSession(atSourceTime: .zero)
var n: Int64 = 0
var last: CVPixelBuffer? = nil
func append(_ pb: CVPixelBuffer) {
  while !input.isReadyForMoreMediaData { usleep(1000) }
  adaptor.append(pb, withPresentationTime: CMTime(value: n, timescale: fps)); n += 1
}
while let sb = out.copyNextSampleBuffer() {
  if let pb = CMSampleBufferGetImageBuffer(sb) { append(pb); last = pb }
}
let original = n
for _ in 0..<extraFrames { append(last!) }
input.markAsFinished()
let sem = DispatchSemaphore(value: 0)
writer.finishWriting { sem.signal() }
sem.wait()
print("status:", writer.status.rawValue, writer.error?.localizedDescription ?? "ok", "frames:", original, "+", extraFrames, "=", n)
if writer.status != .completed { exit(1) }

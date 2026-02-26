'use client';

import { RefObject } from 'react';
import { Camera, X } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface CameraViewProps {
  isOpen: boolean;
  videoRef: RefObject<HTMLVideoElement | null>;
  canvasRef: RefObject<HTMLCanvasElement | null>;
  onCapture: () => void;
  onClose: () => void;
  error: string | null;
}

export function CameraView({
  isOpen,
  videoRef,
  canvasRef,
  onCapture,
  onClose,
  error,
}: CameraViewProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black flex flex-col">
      {/* Hidden canvas for capturing */}
      <canvas ref={canvasRef} className="hidden" />
      
      {/* Camera view */}
      <div className="flex-1 relative">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="w-full h-full object-cover"
          onCanPlay={(e) => {
            const video = e.currentTarget;
            video.play().catch(console.error);
          }}
        />
        
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 bg-black/50 backdrop-blur-sm rounded-full text-white hover:bg-black/70 transition-colors z-10"
        >
          <X className="w-6 h-6" />
        </button>

        {/* Camera frame guide */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="w-72 h-72 border-2 border-white/30 rounded-full" />
        </div>
        
        {/* Instructions */}
        <div className="absolute top-20 left-0 right-0 text-center pointer-events-none">
          <p className="text-white/80 text-sm bg-black/30 backdrop-blur-sm px-4 py-2 rounded-full inline-block">
            Position your face in the circle
          </p>
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/80">
          <div className="text-center p-6">
            <p className="text-red-400 mb-4">{error}</p>
            <Button variant="secondary" onClick={onClose}>
              Close
            </Button>
          </div>
        </div>
      )}

      {/* Capture button */}
      <div className="absolute bottom-8 left-0 right-0 flex justify-center">
        <button
          onClick={onCapture}
          className="w-20 h-20 rounded-full bg-white flex items-center justify-center shadow-lg active:scale-95 transition-transform"
        >
          <div className="w-16 h-16 rounded-full border-4 border-gray-300 flex items-center justify-center">
            <Camera className="w-8 h-8 text-gray-600" />
          </div>
        </button>
      </div>
    </div>
  );
}

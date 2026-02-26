'use client';

import { useCallback, useRef } from 'react';
import { Camera, ImagePlus, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface ImageUploaderProps {
  image: string | null;
  onImageSelect: (image: string) => void;
  onCameraOpen: () => void;
  onClear: () => void;
  isGenerating: boolean;
}

export function ImageUploader({
  image,
  onImageSelect,
  onCameraOpen,
  onClear,
  isGenerating,
}: ImageUploaderProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        if (event.target?.result) {
          onImageSelect(event.target.result as string);
        }
      };
      reader.readAsDataURL(file);
    }
  }, [onImageSelect]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (event) => {
        if (event.target?.result) {
          onImageSelect(event.target.result as string);
        }
      };
      reader.readAsDataURL(file);
    }
  }, [onImageSelect]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
  }, []);

  if (image) {
    return (
      <div className="relative w-full aspect-square max-w-sm mx-auto">
        <img
          src={image}
          alt="Selected photo"
          className="w-full h-full object-cover rounded-2xl shadow-lg"
        />
        {!isGenerating && (
          <button
            onClick={onClear}
            className="absolute top-3 right-3 p-2 bg-black/50 backdrop-blur-sm rounded-full text-white hover:bg-black/70 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>
    );
  }

  return (
    <div
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      className="w-full aspect-square max-w-sm mx-auto"
    >
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileSelect}
        className="hidden"
      />
      <div className="w-full h-full border-2 border-dashed border-muted-foreground/25 rounded-2xl flex flex-col items-center justify-center gap-6 p-6 bg-muted/30 hover:bg-muted/50 transition-colors">
        <div className="w-20 h-20 rounded-full bg-gradient-to-br from-violet-500/20 to-pink-500/20 flex items-center justify-center">
          <ImagePlus className="w-10 h-10 text-muted-foreground" />
        </div>
        <div className="text-center">
          <p className="text-lg font-medium text-foreground">Upload your photo</p>
          <p className="text-sm text-muted-foreground mt-1">
            Drag & drop or choose from gallery
          </p>
        </div>
        <div className="flex gap-3">
          <Button
            variant="default"
            className="gap-2"
            onClick={() => fileInputRef.current?.click()}
          >
            <ImagePlus className="w-4 h-4" />
            Gallery
          </Button>
          <Button
            variant="secondary"
            className="gap-2"
            onClick={onCameraOpen}
          >
            <Camera className="w-4 h-4" />
            Camera
          </Button>
        </div>
      </div>
    </div>
  );
}

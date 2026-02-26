'use client';

import { Download, Share2, RotateCcw, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { STYLE_OPTIONS } from './config';
import { CaricatureStyle } from '@/types/caricature';

interface ResultViewProps {
  originalImage: string;
  caricatureImage: string;
  style: CaricatureStyle;
  onDownload: () => void;
  onShare: () => void;
  onReset: () => void;
  isSharing: boolean;
}

export function ResultView({
  originalImage,
  caricatureImage,
  style,
  onDownload,
  onShare,
  onReset,
  isSharing,
}: ResultViewProps) {
  const selectedStyle = STYLE_OPTIONS.find((s) => s.id === style);

  return (
    <div className="w-full flex flex-col gap-4">
      {/* Before/After comparison */}
      <div className="grid grid-cols-2 gap-3">
        <div className="relative">
          <img
            src={originalImage}
            alt="Original"
            className="w-full aspect-square object-cover rounded-xl shadow-md"
          />
          <span className="absolute bottom-2 left-2 text-xs font-medium bg-black/50 backdrop-blur-sm text-white px-2 py-1 rounded-full">
            Original
          </span>
        </div>
        <div className="relative">
          <img
            src={caricatureImage}
            alt="Caricature"
            className="w-full aspect-square object-cover rounded-xl shadow-md"
          />
          <span className="absolute bottom-2 left-2 text-xs font-medium bg-gradient-to-r from-violet-500 to-pink-500 text-white px-2 py-1 rounded-full flex items-center gap-1">
            <Sparkles className="w-3 h-3" />
            {selectedStyle?.name}
          </span>
        </div>
      </div>

      {/* Action buttons */}
      <div className="grid grid-cols-3 gap-2">
        <Button
          variant="outline"
          className="flex flex-col gap-1 h-auto py-3"
          onClick={onDownload}
        >
          <Download className="w-5 h-5" />
          <span className="text-xs">Save</span>
        </Button>
        <Button
          variant="outline"
          className="flex flex-col gap-1 h-auto py-3"
          onClick={onShare}
          disabled={isSharing}
        >
          <Share2 className="w-5 h-5" />
          <span className="text-xs">Share</span>
        </Button>
        <Button
          variant="outline"
          className="flex flex-col gap-1 h-auto py-3"
          onClick={onReset}
        >
          <RotateCcw className="w-5 h-5" />
          <span className="text-xs">New</span>
        </Button>
      </div>
    </div>
  );
}

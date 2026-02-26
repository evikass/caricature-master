'use client';

import { Sparkles } from 'lucide-react';

interface LoadingAnimationProps {
  style: string;
  intensity: number;
}

export function LoadingAnimation({ style, intensity }: LoadingAnimationProps) {
  const getStyleEmoji = () => {
    switch (style) {
      case 'funny': return '🤪';
      case 'cartoon': return '🎨';
      case 'artistic': return '🖌️';
      case 'realistic': return '✨';
      default: return '🎨';
    }
  };

  const getIntensityText = () => {
    if (intensity <= 33) return 'Light touch';
    if (intensity <= 66) return 'Balanced style';
    return 'Maximum drama';
  };

  return (
    <div className="fixed inset-0 z-50 bg-background/95 backdrop-blur-sm flex flex-col items-center justify-center p-6">
      {/* Animated spinner */}
      <div className="relative w-24 h-24 mb-8">
        <div className="absolute inset-0 rounded-full border-4 border-muted" />
        <div className="absolute inset-0 rounded-full border-4 border-primary border-t-transparent animate-spin" />
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-3xl animate-pulse">{getStyleEmoji()}</span>
        </div>
      </div>

      {/* Text content */}
      <div className="text-center space-y-2 mb-8">
        <h3 className="text-xl font-semibold flex items-center gap-2 justify-center">
          <Sparkles className="w-5 h-5 text-primary animate-pulse" />
          Creating your caricature
        </h3>
        <p className="text-muted-foreground">
          {getStyleEmoji()} {style.charAt(0).toUpperCase() + style.slice(1)} style
        </p>
        <p className="text-sm text-muted-foreground/70">
          {getIntensityText()} • {intensity}%
        </p>
      </div>

      {/* Progress dots */}
      <div className="flex gap-2">
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className="w-2 h-2 rounded-full bg-primary animate-bounce"
            style={{ animationDelay: `${i * 0.15}s` }}
          />
        ))}
      </div>

      {/* Fun tip */}
      <p className="mt-8 text-xs text-muted-foreground/50 max-w-xs text-center">
        Tip: Different styles work better with different photos. Try them all!
      </p>
    </div>
  );
}

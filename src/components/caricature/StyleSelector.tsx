'use client';

import { CaricatureStyle } from '@/types/caricature';
import { STYLE_OPTIONS } from './config';
import { cn } from '@/lib/utils';

interface StyleSelectorProps {
  selectedStyle: CaricatureStyle;
  onSelect: (style: CaricatureStyle) => void;
}

export function StyleSelector({ selectedStyle, onSelect }: StyleSelectorProps) {
  return (
    <div className="w-full">
      <h3 className="text-sm font-medium text-muted-foreground mb-3 px-1">Choose Style</h3>
      <div className="grid grid-cols-4 gap-2">
        {STYLE_OPTIONS.map((style) => (
          <button
            key={style.id}
            onClick={() => onSelect(style.id)}
            className={cn(
              'flex flex-col items-center gap-2 p-3 rounded-xl transition-all duration-200',
              'border-2',
              selectedStyle === style.id
                ? 'border-primary bg-primary/10 shadow-sm scale-105'
                : 'border-transparent bg-muted/50 hover:bg-muted active:scale-95'
            )}
          >
            <span className="text-2xl">{style.emoji}</span>
            <span className={cn(
              'text-xs font-medium',
              selectedStyle === style.id ? 'text-primary' : 'text-foreground'
            )}>
              {style.name}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}

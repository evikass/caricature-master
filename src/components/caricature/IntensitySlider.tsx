'use client';

import { Slider } from '@/components/ui/slider';

interface IntensitySliderProps {
  intensity: number;
  onChange: (intensity: number) => void;
}

export function IntensitySlider({ intensity, onChange }: IntensitySliderProps) {
  const getIntensityLabel = () => {
    if (intensity <= 33) return 'Subtle';
    if (intensity <= 66) return 'Moderate';
    return 'Dramatic';
  };

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-3 px-1">
        <h3 className="text-sm font-medium text-muted-foreground">Intensity</h3>
        <span className="text-xs font-medium text-primary bg-primary/10 px-2 py-1 rounded-full">
          {getIntensityLabel()}
        </span>
      </div>
      <div className="relative px-1">
        <Slider
          value={[intensity]}
          onValueChange={(values) => onChange(values[0])}
          max={100}
          step={1}
          className="w-full"
        />
        <div className="flex justify-between mt-2 px-1">
          <span className="text-xs text-muted-foreground">Light</span>
          <span className="text-xs text-muted-foreground">Strong</span>
        </div>
      </div>
    </div>
  );
}

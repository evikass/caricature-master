'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { Switch } from '@/components/ui/switch';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import type { ArmatureSettings, ArmaturePreset } from '@/lib/armature-generator';
import { User, Cog, Hand, Sparkles, Download, RotateCcw } from 'lucide-react';

interface ControlsProps {
  settings: ArmatureSettings;
  presets: ArmaturePreset[];
  selectedPreset: string;
  onSettingsChange: (settings: Partial<ArmatureSettings>) => void;
  onPresetChange: (presetId: string) => void;
  onGenerate: () => void;
  onReset: () => void;
  isGenerating: boolean;
}

export default function Controls({
  settings,
  presets,
  selectedPreset,
  onSettingsChange,
  onPresetChange,
  onGenerate,
  onReset,
  isGenerating,
}: ControlsProps) {
  return (
    <div className="space-y-4 max-h-[calc(100vh-200px)] overflow-y-auto pr-2 custom-scrollbar">
      {/* Presets Section */}
      <Card className="border-slate-700 bg-slate-800/50 backdrop-blur">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg flex items-center gap-2 text-white">
            <Sparkles className="w-5 h-5 text-amber-400" />
            Пресеты каркасов
          </CardTitle>
          <CardDescription className="text-slate-400">
            Выберите готовый шаблон или настройте параметры вручную
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-3">
            {presets.map((preset) => (
              <button
                key={preset.id}
                onClick={() => onPresetChange(preset.id)}
                className={`p-4 rounded-lg text-left transition-all duration-200 border ${
                  selectedPreset === preset.id
                    ? 'bg-gradient-to-r from-emerald-600/20 to-teal-600/20 border-emerald-500/50 shadow-lg shadow-emerald-500/10'
                    : 'bg-slate-900/50 border-slate-700 hover:border-slate-600 hover:bg-slate-900/80'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-white">{preset.nameRu}</span>
                  <Badge 
                    variant={preset.type === 'professional' ? 'default' : preset.type === 'simple' ? 'secondary' : 'outline'}
                    className={preset.type === 'professional' ? 'bg-amber-500' : preset.type === 'simple' ? 'bg-emerald-500' : ''}
                  >
                    {preset.type === 'professional' ? 'Про' : preset.type === 'simple' ? 'Базовый' : 'Мини'}
                  </Badge>
                </div>
                <p className="text-sm text-slate-400">{preset.descriptionRu}</p>
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Dimensions Section */}
      <Card className="border-slate-700 bg-slate-800/50 backdrop-blur">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg flex items-center gap-2 text-white">
            <User className="w-5 h-5 text-blue-400" />
            Размеры куклы
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Label className="text-slate-300">Высота куклы</Label>
              <span className="text-emerald-400 font-mono font-semibold">{settings.height} мм</span>
            </div>
            <Slider
              value={[settings.height]}
              onValueChange={([value]) => onSettingsChange({ height: value as 100 | 150 | 200 | 250 | 300 })}
              min={100}
              max={300}
              step={50}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-slate-500">
              <span>100мм</span>
              <span>150мм</span>
              <span>200мм</span>
              <span>250мм</span>
              <span>300мм</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Joint Settings Section */}
      <Card className="border-slate-700 bg-slate-800/50 backdrop-blur">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg flex items-center gap-2 text-white">
            <Cog className="w-5 h-5 text-purple-400" />
            Настройки шарниров
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label className="text-slate-300">Диаметр шарниров</Label>
            <Select
              value={String(settings.jointDiameter)}
              onValueChange={(value) => onSettingsChange({ jointDiameter: Number(value) as 3 | 4 | 5 | 6 })}
            >
              <SelectTrigger className="bg-slate-900 border-slate-700 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-slate-800 border-slate-700">
                <SelectItem value="3">3 мм - для мини-кукол</SelectItem>
                <SelectItem value="4">4 мм - стандартный</SelectItem>
                <SelectItem value="5">5 мм - профессиональный</SelectItem>
                <SelectItem value="6">6 мм - для крупных кукол</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label className="text-slate-300">Тип соединений</Label>
            <Select
              value={settings.jointType}
              onValueChange={(value) => onSettingsChange({ jointType: value as 'ball-and-socket' | 'hinge' })}
            >
              <SelectTrigger className="bg-slate-900 border-slate-700 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-slate-800 border-slate-700">
                <SelectItem value="ball-and-socket">Ball-and-Socket (сферические)</SelectItem>
                <SelectItem value="hinge">Hinge (шарнирные)</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <Separator className="bg-slate-700" />

          <div className="space-y-3">
            <Label className="text-slate-300">Зазор для печати</Label>
            <div className="flex items-center justify-between">
              <Slider
                value={[settings.printGap * 100]}
                onValueChange={([value]) => onSettingsChange({ printGap: value / 100 })}
                min={20}
                max={30}
                step={5}
                className="w-48"
              />
              <span className="text-emerald-400 font-mono font-semibold w-16 text-right">
                {settings.printGap.toFixed(2)} мм
              </span>
            </div>
            <p className="text-xs text-slate-500">Оптимально: 0.25 мм для SLA печати</p>
          </div>
        </CardContent>
      </Card>

      {/* Hand Settings Section */}
      <Card className="border-slate-700 bg-slate-800/50 backdrop-blur">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg flex items-center gap-2 text-white">
            <Hand className="w-5 h-5 text-pink-400" />
            Настройки кистей
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <Label className="text-slate-300">Количество пальцев</Label>
            <Select
              value={String(settings.fingerCount)}
              onValueChange={(value) => onSettingsChange({ fingerCount: Number(value) as 3 | 4 | 5 })}
            >
              <SelectTrigger className="bg-slate-900 border-slate-700 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-slate-800 border-slate-700">
                <SelectItem value="3">3 пальца - упрощённый вариант</SelectItem>
                <SelectItem value="4">4 пальца + большой палец</SelectItem>
                <SelectItem value="5">5 пальцев - реалистичный</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Additional Options Section */}
      <Card className="border-slate-700 bg-slate-800/50 backdrop-blur">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg flex items-center gap-2 text-white">
            <Sparkles className="w-5 h-5 text-cyan-400" />
            Дополнительные опции
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label className="text-slate-300">Уши</Label>
              <p className="text-xs text-slate-500">Добавить каркас для ушей</p>
            </div>
            <Switch
              checked={settings.includeEars}
              onCheckedChange={(checked) => onSettingsChange({ includeEars: checked })}
            />
          </div>

          <Separator className="bg-slate-700" />

          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label className="text-slate-300">Хвост</Label>
              <p className="text-xs text-slate-500">Добавить каркас для хвоста</p>
            </div>
            <Switch
              checked={settings.includeTail}
              onCheckedChange={(checked) => onSettingsChange({ includeTail: checked })}
            />
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="space-y-3 pt-2">
        <Button
          onClick={onGenerate}
          disabled={isGenerating}
          className="w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold py-6 shadow-lg shadow-emerald-500/25 transition-all duration-200"
        >
          <Download className="w-5 h-5 mr-2" />
          {isGenerating ? 'Генерация...' : 'Скачать Python скрипт для Blender'}
        </Button>

        <Button
          onClick={onReset}
          variant="outline"
          className="w-full border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white"
        >
          <RotateCcw className="w-4 h-4 mr-2" />
          Сбросить настройки
        </Button>
      </div>

      {/* Info Box */}
      <div className="p-4 bg-slate-900/80 border border-slate-700 rounded-lg">
        <h4 className="text-sm font-medium text-slate-300 mb-2">Рекомендации для SLA печати:</h4>
        <ul className="text-xs text-slate-400 space-y-1 list-disc list-inside">
          <li>Высота слоя: 0.05 мм для лучшей детализации</li>
          <li>Ориентация: шары печатайте опорной точкой вверх</li>
          <li>Проверьте подгонку всех шарниров перед сборкой</li>
          <li>Используйте эпоксидный клей для постоянных соединений</li>
        </ul>
      </div>
    </div>
  );
}

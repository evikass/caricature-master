'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';
import type { ArmatureConfig } from '@/lib/armatureScript';
import { 
  Download, 
  RotateCcw, 
  Maximize2, 
  Circle, 
  Gap, 
  Bone,
  User,
  UserCheck,
  Cat
} from 'lucide-react';

interface ConfigPanelProps {
  config: ArmatureConfig;
  onConfigChange: (config: Partial<ArmatureConfig>) => void;
  onGenerate: () => void;
  onReset: () => void;
  isGenerating: boolean;
}

const armatureTypes: { id: ArmatureConfig['armatureType']; name: string; icon: React.ReactNode; description: string }[] = [
  { 
    id: 'humanoid', 
    name: 'Гуманоид', 
    icon: <User className="w-5 h-5" />,
    description: 'Человеческий каркас с полным набором шарниров'
  },
  { 
    id: 'simple', 
    name: 'Простой', 
    icon: <UserCheck className="w-5 h-5" />,
    description: 'Упрощённый каркас без коленей и локтей'
  },
  { 
    id: 'animal', 
    name: 'Животное', 
    icon: <Cat className="w-5 h-5" />,
    description: 'Четвероногий каркас для животных'
  },
];

export default function ConfigPanel({
  config,
  onConfigChange,
  onGenerate,
  onReset,
  isGenerating,
}: ConfigPanelProps) {
  return (
    <div className="space-y-4">
      {/* Armature Type Selection */}
      <Card className="border-slate-700 bg-slate-800/50 backdrop-blur">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg flex items-center gap-2 text-white">
            <Maximize2 className="w-5 h-5 text-emerald-400" />
            Тип каркаса
          </CardTitle>
          <CardDescription className="text-slate-400">
            Выберите тип арматуры для генерации
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-2">
            {armatureTypes.map((type) => (
              <button
                key={type.id}
                onClick={() => onConfigChange({ armatureType: type.id })}
                className={`p-3 rounded-lg text-left transition-all duration-200 border flex items-center gap-3 ${
                  config.armatureType === type.id
                    ? 'bg-gradient-to-r from-emerald-600/20 to-teal-600/20 border-emerald-500/50 shadow-lg shadow-emerald-500/10'
                    : 'bg-slate-900/50 border-slate-700 hover:border-slate-600 hover:bg-slate-900/80'
                }`}
              >
                <div className={`p-2 rounded-lg ${
                  config.armatureType === type.id ? 'bg-emerald-600/30 text-emerald-400' : 'bg-slate-700 text-slate-400'
                }`}>
                  {type.icon}
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-white">{type.name}</span>
                    {config.armatureType === type.id && (
                      <Badge className="bg-emerald-600 text-xs">Выбрано</Badge>
                    )}
                  </div>
                  <p className="text-xs text-slate-400 mt-0.5">{type.description}</p>
                </div>
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Scale Factor */}
      <Card className="border-slate-700 bg-slate-800/50 backdrop-blur">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg flex items-center gap-2 text-white">
            <Maximize2 className="w-5 h-5 text-blue-400" />
            Масштаб
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Label className="text-slate-300">Коэффициент масштаба</Label>
              <span className="text-emerald-400 font-mono font-semibold">{config.scaleFactor.toFixed(1)}x</span>
            </div>
            <Slider
              value={[config.scaleFactor]}
              onValueChange={([value]) => onConfigChange({ scaleFactor: value })}
              min={0.5}
              max={2.0}
              step={0.1}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-slate-500">
              <span>0.5x</span>
              <span>1.0x</span>
              <span>1.5x</span>
              <span>2.0x</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Joint Settings */}
      <Card className="border-slate-700 bg-slate-800/50 backdrop-blur">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg flex items-center gap-2 text-white">
            <Circle className="w-5 h-5 text-red-400" />
            Шарниры
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Ball Joint Radius */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Label className="text-slate-300">Радиус шара шарнира</Label>
              <span className="text-emerald-400 font-mono font-semibold">{config.ballJointRadius.toFixed(1)} мм</span>
            </div>
            <Slider
              value={[config.ballJointRadius]}
              onValueChange={([value]) => onConfigChange({ ballJointRadius: value })}
              min={2.0}
              max={5.0}
              step={0.1}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-slate-500">
              <span>2.0 мм</span>
              <span>3.5 мм</span>
              <span>5.0 мм</span>
            </div>
          </div>

          <Separator className="bg-slate-700" />

          {/* Socket Gap */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Label className="text-slate-300">Зазор втулки</Label>
              <span className="text-emerald-400 font-mono font-semibold">{config.socketGap.toFixed(2)} мм</span>
            </div>
            <Slider
              value={[config.socketGap]}
              onValueChange={([value]) => onConfigChange({ socketGap: value })}
              min={0.1}
              max={0.3}
              step={0.01}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-slate-500">
              <span>0.10 мм</span>
              <span>0.20 мм</span>
              <span>0.30 мм</span>
            </div>
            <p className="text-xs text-slate-500">Оптимально: 0.20 мм для SLA печати</p>
          </div>
        </CardContent>
      </Card>

      {/* Bone Settings */}
      <Card className="border-slate-700 bg-slate-800/50 backdrop-blur">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg flex items-center gap-2 text-white">
            <Bone className="w-5 h-5 text-purple-400" />
            Кости
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Bone Diameter */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Label className="text-slate-300">Диаметр кости</Label>
              <span className="text-emerald-400 font-mono font-semibold">{config.boneDiameter.toFixed(1)} мм</span>
            </div>
            <Slider
              value={[config.boneDiameter]}
              onValueChange={([value]) => onConfigChange({ boneDiameter: value })}
              min={2.0}
              max={4.0}
              step={0.1}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-slate-500">
              <span>2.0 мм</span>
              <span>3.0 мм</span>
              <span>4.0 мм</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Configuration Summary */}
      <Card className="border-slate-700 bg-slate-800/50 backdrop-blur">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg flex items-center gap-2 text-white">
            Текущие параметры
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-2">
            <div className="p-2 bg-slate-900/50 rounded-lg text-center">
              <div className="text-lg font-bold text-emerald-400">{config.scaleFactor.toFixed(1)}x</div>
              <div className="text-xs text-slate-400">Масштаб</div>
            </div>
            <div className="p-2 bg-slate-900/50 rounded-lg text-center">
              <div className="text-lg font-bold text-red-400">{config.ballJointRadius.toFixed(1)} мм</div>
              <div className="text-xs text-slate-400">Шарнир</div>
            </div>
            <div className="p-2 bg-slate-900/50 rounded-lg text-center">
              <div className="text-lg font-bold text-blue-400">{config.socketGap.toFixed(2)} мм</div>
              <div className="text-xs text-slate-400">Зазор</div>
            </div>
            <div className="p-2 bg-slate-900/50 rounded-lg text-center">
              <div className="text-lg font-bold text-purple-400">{config.boneDiameter.toFixed(1)} мм</div>
              <div className="text-xs text-slate-400">Кость</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="space-y-3">
        <Button
          onClick={onGenerate}
          disabled={isGenerating}
          className="w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold py-6 shadow-lg shadow-emerald-500/25 transition-all duration-200"
        >
          <Download className="w-5 h-5 mr-2" />
          {isGenerating ? 'Генерация...' : 'Сгенерировать скрипт Blender'}
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
          <li>Шары печатайте опорной точкой вверх</li>
          <li>Втулки печатайте отверстием вверх</li>
          <li>Проверьте подгонку всех шарниров перед сборкой</li>
        </ul>
      </div>
    </div>
  );
}

'use client';

import { useState, useRef, useCallback, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Camera, 
  ImagePlus, 
  Wand2, 
  Download, 
  Share2, 
  History, 
  Sparkles,
  ChevronLeft,
  ChevronRight,
  Loader2,
  Trash2,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  X,
  Palette,
  Sliders,
  User,
  Copy,
  Check,
  MessageSquare,
  Instagram,
  Send,
  Type,
  Frame,
  Droplet,
  Heart,
  Star,
  Trophy,
  Flame,
  Gift,
  Crown,
  Zap,
  TrendingUp,
  Award,
  Target,
  BookOpen
} from 'lucide-react';
import { cn } from '@/lib/utils';

// Types
interface CaricatureStyle {
  id: string;
  name: string;
  nameRu: string;
  icon: string;
  description: string;
  premium?: boolean;
}

interface HistoryItem {
  id: string;
  originalImage: string;
  caricatureImage: string;
  style: string;
  intensity: number;
  caption?: string;
  likes: number;
  shares: number;
  createdAt: number;
}

interface UserStats {
  totalCreated: number;
  totalLikes: number;
  totalShares: number;
  streak: number;
  achievements: string[];
  level: number;
  xp: number;
}

interface CaptionTemplate {
  id: string;
  text: string;
  category: 'funny' | 'cool' | 'cute' | 'viral';
}

// Extended styles
const CARICATURE_STYLES: CaricatureStyle[] = [
  { id: 'funny', name: 'Funny', nameRu: 'Смешной', icon: '😂', description: 'Комичный и забавный' },
  { id: 'cartoon', name: 'Cartoon', nameRu: 'Мультяшный', icon: '🎨', description: 'Яркий мультяшный' },
  { id: 'artistic', name: 'Artistic', nameRu: 'Художественный', icon: '🖼️', description: 'Творческая стилизация' },
  { id: 'comic', name: 'Comic', nameRu: 'Комикс', icon: '💥', description: 'Стиль комиксов' },
  { id: 'sketch', name: 'Sketch', nameRu: 'Скетч', icon: '✏️', description: 'Рисунок карандашом' },
  { id: 'anime', name: 'Anime', nameRu: 'Аниме', icon: '🌸', description: 'Японская анимация' },
  { id: 'realistic', name: 'Realistic', nameRu: 'Реалистичный', icon: '🎭', description: 'Тонкая стилизация' },
  { id: 'celebrity', name: 'Celebrity', nameRu: 'Звёздный', icon: '⭐', description: 'Обложка журнала' },
  { id: 'chibi', name: 'Chibi', nameRu: 'Чиби', icon: '🧸', description: 'Милый чиби-стиль' },
  { id: 'grotesque', name: 'Grotesque', nameRu: 'Гротеск', icon: '🎭', description: 'Сюрреалистичный' },
];

// Caption templates for social media
const CAPTION_TEMPLATES: CaptionTemplate[] = [
  { id: '1', text: 'Смотрите, какой шарж! 😂 Теги: #шарж #карикатура #юмор', category: 'funny' },
  { id: '2', text: 'AI нарисовал меня! 🤖✨ Как вам результат? #AIart #шарж', category: 'cool' },
  { id: '3', text: 'Немного творчества на сегодня 🎨 #творчество #портрет', category: 'cute' },
  { id: '4', text: 'Когда просишь нарисовать тебя смешным 😅 #юмор #прикол', category: 'funny' },
  { id: '5', text: 'Ловите позитив! 🌟 Ставьте лайк если понравилось! ❤️', category: 'viral' },
  { id: '6', text: 'Оцените от 1 до 10 👇 #опрос #мнение', category: 'viral' },
  { id: '7', text: 'Репост, если узнали себя! 😉🔄', category: 'viral' },
  { id: '8', text: 'День хорошо начался! ☀️ #позитив #утро', category: 'cute' },
  { id: '9', text: 'Мой портрет в стиле {style}! 🎨 Как вам?', category: 'cool' },
  { id: '10', text: 'Когда друг сказал, что ты выглядишь так 😂👇', category: 'funny' },
];

// Achievements
const ACHIEVEMENTS = [
  { id: 'first', name: 'Первый шаг', icon: '🎯', description: 'Создать первый шарж', xp: 50 },
  { id: 'creative', name: 'Творец', icon: '🎨', description: 'Создать 10 шаржей', xp: 100 },
  { id: 'popular', name: 'Популярный', icon: '⭐', description: 'Получить 10 лайков', xp: 150 },
  { id: 'viral', name: 'Вирусный', icon: '🔥', description: 'Поделиться 5 раз', xp: 200 },
  { id: 'master', name: 'Мастер', icon: '👑', description: 'Создать 50 шаржей', xp: 500 },
  { id: 'legend', name: 'Легенда', icon: '🏆', description: 'Создать 100 шаржей', xp: 1000 },
  { id: 'streak3', name: 'На волне', icon: '🌊', description: '3 дня подряд', xp: 75 },
  { id: 'streak7', name: 'Марафонец', icon: '🏃', description: '7 дней подряд', xp: 200 },
];

// Frame presets for social media
const FRAMES = [
  { id: 'none', name: 'Без рамки', color: 'transparent' },
  { id: 'white', name: 'Белая', color: '#ffffff' },
  { id: 'black', name: 'Чёрная', color: '#000000' },
  { id: 'gold', name: 'Золотая', color: '#ffd700' },
  { id: 'pink', name: 'Розовая', color: '#ff69b4' },
  { id: 'gradient', name: 'Градиент', color: 'linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3)' },
];

// Level thresholds
const LEVEL_THRESHOLDS = [0, 100, 300, 600, 1000, 1500, 2200, 3000, 4000, 5500, 7500, 10000];

export default function CaricatureApp() {
  // State
  const [activeTab, setActiveTab] = useState<'create' | 'history' | 'profile'>('create');
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [generatedImage, setGeneratedImage] = useState<string | null>(null);
  const [selectedStyle, setSelectedStyle] = useState<string>('funny');
  const [intensity, setIntensity] = useState<number>(50);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [zoom, setZoom] = useState<number>(1);
  const [showTutorial, setShowTutorial] = useState<boolean>(false);
  const [showCaptionModal, setShowCaptionModal] = useState<boolean>(false);
  const [showFrameModal, setShowFrameModal] = useState<boolean>(false);
  const [selectedCaption, setSelectedCaption] = useState<string>('');
  const [selectedFrame, setSelectedFrame] = useState<string>('none');
  const [copiedCaption, setCopiedCaption] = useState<boolean>(false);
  const [stats, setStats] = useState<UserStats>({
    totalCreated: 0,
    totalLikes: 0,
    totalShares: 0,
    streak: 0,
    achievements: [],
    level: 1,
    xp: 0,
  });
  const [showAchievement, setShowAchievement] = useState<string | null>(null);
  const [selectedHistoryItem, setSelectedHistoryItem] = useState<HistoryItem | null>(null);
  
  // Refs
  const fileInputRef = useRef<HTMLInputElement>(null);
  const styleCarouselRef = useRef<HTMLDivElement>(null);

  // Load data from localStorage
  useEffect(() => {
    const savedHistory = localStorage.getItem('caricature_history_v2');
    const savedStats = localStorage.getItem('caricature_stats_v2');
    
    if (savedHistory) {
      try {
        setHistory(JSON.parse(savedHistory));
      } catch (e) {
        console.error('Failed to load history:', e);
      }
    }
    
    if (savedStats) {
      try {
        setStats(JSON.parse(savedStats));
      } catch (e) {
        console.error('Failed to load stats:', e);
      }
    }
    
    const hasSeenTutorial = localStorage.getItem('caricature_tutorial_seen_v2');
    if (!hasSeenTutorial) {
      setShowTutorial(true);
    }
  }, []);

  // Save data to localStorage
  useEffect(() => {
    localStorage.setItem('caricature_history_v2', JSON.stringify(history));
  }, [history]);

  useEffect(() => {
    localStorage.setItem('caricature_stats_v2', JSON.stringify(stats));
  }, [stats]);

  // Calculate level from XP
  const calculateLevel = useCallback((xp: number): number => {
    for (let i = LEVEL_THRESHOLDS.length - 1; i >= 0; i--) {
      if (xp >= LEVEL_THRESHOLDS[i]) {
        return i + 1;
      }
    }
    return 1;
  }, []);

  // Add XP and check achievements
  const addXP = useCallback((amount: number) => {
    setStats(prev => {
      const newXP = prev.xp + amount;
      const newLevel = calculateLevel(newXP);
      return {
        ...prev,
        xp: newXP,
        level: newLevel,
      };
    });
  }, [calculateLevel]);

  // Check and unlock achievements
  const checkAchievements = useCallback(() => {
    const newAchievements: string[] = [];
    
    if (stats.totalCreated >= 1 && !stats.achievements.includes('first')) {
      newAchievements.push('first');
    }
    if (stats.totalCreated >= 10 && !stats.achievements.includes('creative')) {
      newAchievements.push('creative');
    }
    if (stats.totalCreated >= 50 && !stats.achievements.includes('master')) {
      newAchievements.push('master');
    }
    if (stats.totalCreated >= 100 && !stats.achievements.includes('legend')) {
      newAchievements.push('legend');
    }
    if (stats.totalLikes >= 10 && !stats.achievements.includes('popular')) {
      newAchievements.push('popular');
    }
    if (stats.totalShares >= 5 && !stats.achievements.includes('viral')) {
      newAchievements.push('viral');
    }
    if (stats.streak >= 3 && !stats.achievements.includes('streak3')) {
      newAchievements.push('streak3');
    }
    if (stats.streak >= 7 && !stats.achievements.includes('streak7')) {
      newAchievements.push('streak7');
    }
    
    if (newAchievements.length > 0) {
      setStats(prev => ({
        ...prev,
        achievements: [...prev.achievements, ...newAchievements],
      }));
      
      // Show first new achievement
      const achievement = ACHIEVEMENTS.find(a => a.id === newAchievements[0]);
      if (achievement) {
        setShowAchievement(achievement.name);
        addXP(achievement.xp);
        setTimeout(() => setShowAchievement(null), 3000);
      }
    }
  }, [stats, addXP]);

  useEffect(() => {
    checkAchievements();
  }, [stats.totalCreated, stats.totalLikes, stats.totalShares, stats.streak, checkAchievements]);

  // Handle file selection
  const handleFileSelect = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.size > 10 * 1024 * 1024) {
        setError('Файл слишком большой. Максимум 10 МБ.');
        return;
      }
      
      const reader = new FileReader();
      reader.onload = (e) => {
        setSelectedImage(e.target?.result as string);
        setGeneratedImage(null);
        setError(null);
        setSelectedCaption('');
      };
      reader.readAsDataURL(file);
    }
  }, []);

  // Handle camera capture
  const handleCameraCapture = useCallback(() => {
    if (fileInputRef.current) {
      fileInputRef.current.setAttribute('capture', 'environment');
      fileInputRef.current.click();
    }
  }, []);

  // Handle gallery selection
  const handleGallerySelect = useCallback(() => {
    if (fileInputRef.current) {
      fileInputRef.current.removeAttribute('capture');
      fileInputRef.current.click();
    }
  }, []);

  // Generate caricature
  const handleGenerate = useCallback(async () => {
    if (!selectedImage) return;
    
    setIsGenerating(true);
    setError(null);
    
    try {
      const response = await fetch('/api/caricature', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image: selectedImage.split(',')[1],
          style: selectedStyle,
          intensity,
          addWatermark: true,
        }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to generate caricature');
      }
      
      const caricatureImage = `data:image/png;base64,${data.image}`;
      setGeneratedImage(caricatureImage);
      
      // Auto-select caption based on style
      const styleTemplate = CAPTION_TEMPLATES.find(t => t.text.includes('{style}'));
      if (styleTemplate) {
        const styleName = CARICATURE_STYLES.find(s => s.id === selectedStyle)?.nameRu || selectedStyle;
        setSelectedCaption(styleTemplate.text.replace('{style}', styleName));
      } else {
        setSelectedCaption(CAPTION_TEMPLATES[Math.floor(Math.random() * 5)].text);
      }
      
      // Add to history
      const historyItem: HistoryItem = {
        id: Date.now().toString(),
        originalImage: selectedImage,
        caricatureImage,
        style: selectedStyle,
        intensity,
        likes: 0,
        shares: 0,
        createdAt: Date.now(),
      };
      
      setHistory(prev => [historyItem, ...prev].slice(0, 50));
      
      // Update stats
      setStats(prev => ({
        ...prev,
        totalCreated: prev.totalCreated + 1,
      }));
      
      addXP(25);
      
    } catch (err: any) {
      setError(err.message || 'Ошибка при генерации');
    } finally {
      setIsGenerating(false);
    }
  }, [selectedImage, selectedStyle, intensity, addXP]);

  // Download image (optimized for social media)
  const handleDownload = useCallback(async (imageData: string) => {
    try {
      // Create a canvas for optimization
      const img = new window.Image();
      img.crossOrigin = 'anonymous';
      
      img.onload = () => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        // Optimal size for VK/Telegram (square)
        const size = 1080;
        canvas.width = size;
        canvas.height = size;
        
        // Draw frame if selected
        if (selectedFrame !== 'none' && ctx) {
          const frame = FRAMES.find(f => f.id === selectedFrame);
          if (frame) {
            ctx.fillStyle = frame.id === 'gradient' ? '#ff6b6b' : frame.color;
            ctx.fillRect(0, 0, size, size);
            
            // Draw image with padding for frame
            const padding = 20;
            ctx.drawImage(img, padding, padding, size - padding * 2, size - padding * 2);
          }
        } else if (ctx) {
          ctx.drawImage(img, 0, 0, size, size);
        }
        
        // Download
        canvas.toBlob((blob) => {
          if (blob) {
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `caricature_${Date.now()}.png`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
          }
        }, 'image/png', 0.95);
      };
      
      img.src = imageData;
    } catch (err) {
      console.error('Download failed:', err);
    }
  }, [selectedFrame]);

  // Share to VK
  const shareToVK = useCallback((imageData: string) => {
    // VK sharing via URL
    const text = encodeURIComponent(selectedCaption || 'Мой шарж!');
    const vkUrl = `https://vk.com/share.php?comment=${text}&noparse=true`;
    window.open(vkUrl, '_blank', 'width=600,height=400');
    
    setStats(prev => ({
      ...prev,
      totalShares: prev.totalShares + 1,
    }));
    addXP(15);
  }, [selectedCaption, addXP]);

  // Share to Telegram
  const shareToTelegram = useCallback((imageData: string) => {
    const text = encodeURIComponent(selectedCaption || 'Мой шарж!');
    const tgUrl = `https://t.me/share/url?url=&text=${text}`;
    window.open(tgUrl, '_blank', 'width=600,height=400');
    
    setStats(prev => ({
      ...prev,
      totalShares: prev.totalShares + 1,
    }));
    addXP(15);
  }, [selectedCaption, addXP]);

  // Copy caption
  const copyCaption = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(selectedCaption);
      setCopiedCaption(true);
      setTimeout(() => setCopiedCaption(false), 2000);
    } catch (err) {
      console.error('Copy failed:', err);
    }
  }, [selectedCaption]);

  // Like item
  const handleLike = useCallback((id: string) => {
    setHistory(prev => prev.map(item => 
      item.id === id ? { ...item, likes: item.likes + 1 } : item
    ));
    setStats(prev => ({
      ...prev,
      totalLikes: prev.totalLikes + 1,
    }));
    addXP(5);
  }, [addXP]);

  // Delete from history
  const handleDeleteFromHistory = useCallback((id: string) => {
    setHistory(prev => prev.filter(item => item.id !== id));
  }, []);

  // Scroll style carousel
  const scrollStyle = useCallback((direction: 'left' | 'right') => {
    if (styleCarouselRef.current) {
      const scrollAmount = 200;
      styleCarouselRef.current.scrollBy({
        left: direction === 'left' ? -scrollAmount : scrollAmount,
        behavior: 'smooth',
      });
    }
  }, []);

  // Close tutorial
  const closeTutorial = useCallback(() => {
    setShowTutorial(false);
    localStorage.setItem('caricature_tutorial_seen_v2', 'true');
  }, []);

  // Get level name
  const getLevelName = useCallback((level: number): string => {
    const names = ['Новичок', 'Ученик', 'Подмастерье', 'Мастер', 'Эксперт', 'Профессионал', 'Виртуоз', 'Гений', 'Легенда', 'Бог', 'Создатель', 'Всевышний'];
    return names[Math.min(level - 1, names.length - 1)];
  }, []);

  // XP progress for current level
  const getXPProgress = useCallback((): number => {
    const currentLevelXP = LEVEL_THRESHOLDS[stats.level - 1] || 0;
    const nextLevelXP = LEVEL_THRESHOLDS[stats.level] || LEVEL_THRESHOLDS[LEVEL_THRESHOLDS.length - 1];
    const progress = ((stats.xp - currentLevelXP) / (nextLevelXP - currentLevelXP)) * 100;
    return Math.min(100, Math.max(0, progress));
  }, [stats.level, stats.xp]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-950 via-violet-900 to-indigo-950 text-white overflow-x-hidden">
      {/* Status bar spacer */}
      <div className="h-safe-top" />
      
      {/* Main content */}
      <main className="pb-24">
        {/* Header */}
        <header className="sticky top-0 z-40 bg-black/40 backdrop-blur-xl border-b border-white/10">
          <div className="px-4 py-3 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-pink-500 via-purple-500 to-violet-600 flex items-center justify-center shadow-lg shadow-purple-500/30">
                <Wand2 className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold flex items-center gap-2">
                  ШаржМастер
                  <span className="text-xs px-2 py-0.5 bg-gradient-to-r from-amber-500 to-orange-500 rounded-full font-medium">
                    PRO
                  </span>
                </h1>
                <div className="flex items-center gap-2 text-xs text-white/60">
                  <Crown className="w-3 h-3 text-amber-400" />
                  <span>{getLevelName(stats.level)} • Уровень {stats.level}</span>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <div className="px-3 py-1 bg-white/10 rounded-full text-xs">
                <span className="text-amber-400 font-bold">{stats.xp}</span> XP
              </div>
            </div>
          </div>
          
          {/* XP Progress Bar */}
          <div className="px-4 pb-2">
            <div className="h-1 bg-white/10 rounded-full overflow-hidden">
              <motion.div 
                className="h-full bg-gradient-to-r from-amber-500 via-orange-500 to-pink-500"
                initial={{ width: 0 }}
                animate={{ width: `${getXPProgress()}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
          </div>
        </header>

        {/* Achievement Popup */}
        <AnimatePresence>
          {showAchievement && (
            <motion.div
              initial={{ opacity: 0, y: -50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -50 }}
              className="fixed top-20 left-4 right-4 z-50 mx-auto max-w-sm"
            >
              <div className="bg-gradient-to-r from-amber-500 to-orange-500 rounded-2xl p-4 shadow-xl flex items-center gap-3">
                <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center text-2xl">
                  🏆
                </div>
                <div>
                  <div className="font-bold">Достижение!</div>
                  <div className="text-sm text-white/80">{showAchievement}</div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Create Tab */}
        {activeTab === 'create' && (
          <div className="px-4 py-4 space-y-4">
            {/* Image Upload Area */}
            {!selectedImage ? (
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-gradient-to-br from-white/5 to-white/[0.02] border-2 border-dashed border-white/20 rounded-3xl p-8 text-center"
              >
                <motion.div 
                  animate={{ y: [0, -10, 0] }}
                  transition={{ duration: 2, repeat: Infinity }}
                  className="w-24 h-24 mx-auto mb-4 rounded-3xl bg-gradient-to-br from-pink-500/20 to-violet-500/20 flex items-center justify-center"
                >
                  <ImagePlus className="w-12 h-12 text-pink-400" />
                </motion.div>
                <h2 className="text-2xl font-bold mb-2">Загрузите фото</h2>
                <p className="text-white/60 text-sm mb-6 max-w-xs mx-auto">
                  Выберите фото из галереи или сделайте новое для создания шаржа
                </p>
                <div className="flex gap-3 justify-center">
                  <motion.button
                    whileTap={{ scale: 0.95 }}
                    onClick={handleCameraCapture}
                    className="flex items-center gap-2 px-6 py-3.5 bg-gradient-to-r from-pink-600 to-rose-600 rounded-xl font-medium shadow-lg shadow-pink-500/25"
                  >
                    <Camera className="w-5 h-5" />
                    Камера
                  </motion.button>
                  <motion.button
                    whileTap={{ scale: 0.95 }}
                    onClick={handleGallerySelect}
                    className="flex items-center gap-2 px-6 py-3.5 bg-white/10 rounded-xl font-medium border border-white/20"
                  >
                    <ImagePlus className="w-5 h-5" />
                    Галерея
                  </motion.button>
                </div>
              </motion.div>
            ) : (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="space-y-4"
              >
                {/* Original Image Preview */}
                <div className="relative rounded-2xl overflow-hidden bg-black/30">
                  <div className="absolute top-2 left-2 px-3 py-1 bg-black/50 rounded-full text-xs font-medium backdrop-blur-sm flex items-center gap-1">
                    <User className="w-3 h-3" /> Оригинал
                  </div>
                  <img 
                    src={selectedImage} 
                    alt="Original" 
                    className="w-full aspect-square object-cover"
                    style={{ transform: `scale(${zoom})` }}
                  />
                  <button
                    onClick={() => {
                      setSelectedImage(null);
                      setGeneratedImage(null);
                      setSelectedCaption('');
                    }}
                    className="absolute top-2 right-2 p-2 bg-black/50 rounded-full backdrop-blur-sm"
                  >
                    <X className="w-5 h-5" />
                  </button>
                  
                  {/* Zoom controls */}
                  <div className="absolute bottom-3 right-3 flex gap-2">
                    <button onClick={() => setZoom(Math.max(1, zoom - 0.2))} className="p-2 bg-black/50 rounded-full backdrop-blur-sm">
                      <ZoomOut className="w-4 h-4" />
                    </button>
                    <button onClick={() => setZoom(Math.min(2, zoom + 0.2))} className="p-2 bg-black/50 rounded-full backdrop-blur-sm">
                      <ZoomIn className="w-4 h-4" />
                    </button>
                    <button onClick={() => setZoom(1)} className="p-2 bg-black/50 rounded-full backdrop-blur-sm">
                      <RotateCcw className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                
                {/* Style Selection */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold flex items-center gap-2">
                      <Palette className="w-4 h-4 text-pink-400" />
                      Стиль шаржа
                    </h3>
                    <div className="flex gap-1">
                      <button onClick={() => scrollStyle('left')} className="p-1.5 bg-white/10 rounded-full">
                        <ChevronLeft className="w-4 h-4" />
                      </button>
                      <button onClick={() => scrollStyle('right')} className="p-1.5 bg-white/10 rounded-full">
                        <ChevronRight className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                  
                  <div 
                    ref={styleCarouselRef}
                    className="flex gap-2 overflow-x-auto scrollbar-hide pb-2 -mx-4 px-4"
                    style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
                  >
                    {CARICATURE_STYLES.map((style) => (
                      <motion.button
                        key={style.id}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => setSelectedStyle(style.id)}
                        className={cn(
                          "flex-shrink-0 p-3 rounded-2xl border-2 transition-all min-w-[85px]",
                          selectedStyle === style.id
                            ? "border-pink-500 bg-gradient-to-br from-pink-500/30 to-violet-500/30 shadow-lg shadow-pink-500/20"
                            : "border-white/10 bg-white/5 hover:border-white/20"
                        )}
                      >
                        <div className="text-2xl mb-1">{style.icon}</div>
                        <div className="text-xs font-medium">{style.nameRu}</div>
                      </motion.button>
                    ))}
                  </div>
                </div>
                
                {/* Intensity Slider */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold flex items-center gap-2">
                      <Sliders className="w-4 h-4 text-violet-400" />
                      Интенсивность
                    </h3>
                    <span className="text-sm px-2 py-0.5 bg-white/10 rounded-full">{intensity}%</span>
                  </div>
                  <input
                    type="range"
                    min="10"
                    max="100"
                    value={intensity}
                    onChange={(e) => setIntensity(Number(e.target.value))}
                    className="w-full h-2 bg-white/10 rounded-full appearance-none cursor-pointer
                      [&::-webkit-slider-thumb]:appearance-none
                      [&::-webkit-slider-thumb]:w-6
                      [&::-webkit-slider-thumb]:h-6
                      [&::-webkit-slider-thumb]:rounded-full
                      [&::-webkit-slider-thumb]:bg-gradient-to-r
                      [&::-webkit-slider-thumb]:from-pink-500
                      [&::-webkit-slider-thumb]:to-violet-500
                      [&::-webkit-slider-thumb]:shadow-lg
                      [&::-webkit-slider-thumb]:shadow-pink-500/25"
                  />
                  <div className="flex justify-between text-xs text-white/40">
                    <span>Нежный</span>
                    <span>Яркий</span>
                    <span>Экстремальный</span>
                  </div>
                </div>

                {/* Frame Selection */}
                <button
                  onClick={() => setShowFrameModal(true)}
                  className="w-full p-3 bg-white/5 rounded-xl border border-white/10 flex items-center justify-between"
                >
                  <div className="flex items-center gap-2">
                    <Frame className="w-4 h-4 text-purple-400" />
                    <span>Рамка для соцсетей</span>
                  </div>
                  <span className="text-white/60 text-sm">
                    {FRAMES.find(f => f.id === selectedFrame)?.name}
                  </span>
                </button>
                
                {/* Generate Button */}
                <motion.button
                  whileTap={{ scale: 0.98 }}
                  onClick={handleGenerate}
                  disabled={isGenerating}
                  className={cn(
                    "w-full py-4 rounded-2xl font-semibold text-lg flex items-center justify-center gap-3 shadow-xl relative overflow-hidden",
                    isGenerating
                      ? "bg-white/10 cursor-not-allowed"
                      : "bg-gradient-to-r from-pink-600 via-purple-600 to-violet-600 shadow-purple-500/30"
                  )}
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="w-6 h-6 animate-spin" />
                      Создаём магию...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-6 h-6" />
                      Создать шарж
                    </>
                  )}
                  
                  {/* Shimmer effect */}
                  <motion.div
                    className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent"
                    animate={{ x: ['-100%', '100%'] }}
                    transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
                  />
                </motion.button>
                
                {/* Error Message */}
                {error && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-200 text-sm"
                  >
                    {error}
                  </motion.div>
                )}
                
                {/* Generated Image */}
                {generatedImage && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-4"
                  >
                    <div className="relative rounded-2xl overflow-hidden bg-black/30">
                      <div className="absolute top-2 left-2 px-3 py-1 bg-gradient-to-r from-pink-500 to-violet-500 rounded-full text-xs font-medium flex items-center gap-1">
                        <Sparkles className="w-3 h-3" /> Готово!
                      </div>
                      <img 
                        src={generatedImage} 
                        alt="Caricature" 
                        className="w-full aspect-square object-cover"
                      />
                      
                      {/* Quick actions overlay */}
                      <div className="absolute bottom-3 left-3 right-3 flex gap-2">
                        <button
                          onClick={() => handleLike(history[0]?.id || '')}
                          className="flex-1 py-2 bg-black/50 rounded-xl backdrop-blur-sm flex items-center justify-center gap-2 text-sm"
                        >
                          <Heart className="w-4 h-4 text-pink-400" />
                          <span>{history[0]?.likes || 0}</span>
                        </button>
                      </div>
                    </div>
                    
                    {/* Caption Section */}
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <h3 className="font-semibold flex items-center gap-2">
                          <MessageSquare className="w-4 h-4 text-blue-400" />
                          Подпись для поста
                        </h3>
                        <button
                          onClick={() => setShowCaptionModal(true)}
                          className="text-sm text-pink-400"
                        >
                          Изменить
                        </button>
                      </div>
                      
                      <div className="p-3 bg-white/5 rounded-xl border border-white/10">
                        <p className="text-sm text-white/80">{selectedCaption}</p>
                      </div>
                      
                      <button
                        onClick={copyCaption}
                        className="w-full py-2 bg-white/10 rounded-xl text-sm flex items-center justify-center gap-2"
                      >
                        {copiedCaption ? (
                          <>
                            <Check className="w-4 h-4 text-green-400" />
                            Скопировано!
                          </>
                        ) : (
                          <>
                            <Copy className="w-4 h-4" />
                            Копировать подпись
                          </>
                        )}
                      </button>
                    </div>
                    
                    {/* Social Share Buttons */}
                    <div className="space-y-2">
                      <h3 className="font-semibold">Поделиться</h3>
                      <div className="grid grid-cols-2 gap-3">
                        <motion.button
                          whileTap={{ scale: 0.95 }}
                          onClick={() => shareToVK(generatedImage)}
                          className="py-3 bg-[#4a76a8] rounded-xl font-medium flex items-center justify-center gap-2 shadow-lg"
                        >
                          <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M15.684 0H8.316C1.592 0 0 1.592 0 8.316v7.368C0 22.408 1.592 24 8.316 24h7.368C22.408 24 24 22.408 24 15.684V8.316C24 1.592 22.408 0 15.684 0zm3.692 17.123h-1.744c-.66 0-.864-.525-2.05-1.727-1.033-1-1.49-1.135-1.744-1.135-.356 0-.458.102-.458.593v1.575c0 .424-.135.678-1.253.678-1.846 0-3.896-1.118-5.335-3.202C4.624 10.857 4 8.781 4 8.273c0-.254.102-.491.593-.491h1.744c.44 0 .61.203.78.678.863 2.49 2.303 4.675 2.896 4.675.22 0 .322-.102.322-.66V9.721c-.068-1.186-.695-1.287-.695-1.71 0-.203.17-.407.44-.407h2.744c.373 0 .508.203.508.643v3.473c0 .372.17.508.271.508.22 0 .407-.136.813-.542 1.254-1.406 2.151-3.574 2.151-3.574.119-.254.322-.491.763-.491h1.744c.525 0 .644.27.525.643-.22 1.017-2.354 4.031-2.354 4.031-.186.305-.254.44 0 .78.186.254.796.779 1.203 1.253.745.847 1.32 1.558 1.473 2.05.17.49-.085.744-.576.744z"/>
                          </svg>
                          ВКонтакте
                        </motion.button>
                        <motion.button
                          whileTap={{ scale: 0.95 }}
                          onClick={() => shareToTelegram(generatedImage)}
                          className="py-3 bg-[#0088cc] rounded-xl font-medium flex items-center justify-center gap-2 shadow-lg"
                        >
                          <Send className="w-5 h-5" />
                          Telegram
                        </motion.button>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-3">
                        <motion.button
                          whileTap={{ scale: 0.95 }}
                          onClick={() => handleDownload(generatedImage)}
                          className="py-3 bg-white/10 rounded-xl font-medium flex items-center justify-center gap-2 border border-white/20"
                        >
                          <Download className="w-5 h-5" />
                          Скачать
                        </motion.button>
                        <motion.button
                          whileTap={{ scale: 0.95 }}
                          onClick={() => {
                            if (navigator.share) {
                              navigator.share({
                                title: 'Мой шарж',
                                text: selectedCaption,
                              });
                            }
                          }}
                          className="py-3 bg-gradient-to-r from-green-600 to-emerald-600 rounded-xl font-medium flex items-center justify-center gap-2"
                        >
                          <Share2 className="w-5 h-5" />
                          Ещё...
                        </motion.button>
                      </div>
                    </div>
                  </motion.div>
                )}
              </motion.div>
            )}
            
            {/* Hidden file input */}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className="hidden"
            />
          </div>
        )}

        {/* History Tab */}
        {activeTab === 'history' && (
          <div className="px-4 py-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold">История</h2>
              <span className="text-sm text-white/60">{history.length} шаржей</span>
            </div>
            
            {history.length === 0 ? (
              <div className="text-center py-16">
                <div className="w-20 h-20 mx-auto mb-4 rounded-2xl bg-white/5 flex items-center justify-center">
                  <History className="w-10 h-10 text-white/30" />
                </div>
                <p className="text-white/60 mb-2">История пуста</p>
                <p className="text-white/40 text-sm">Созданные шаржи появятся здесь</p>
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-3">
                <AnimatePresence>
                  {history.map((item, index) => (
                    <motion.div
                      key={item.id}
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.9 }}
                      transition={{ delay: index * 0.05 }}
                      className="relative rounded-2xl overflow-hidden bg-black/30 aspect-square group"
                      onClick={() => setSelectedHistoryItem(item)}
                    >
                      <img 
                        src={item.caricatureImage} 
                        alt="Caricature"
                        className="w-full h-full object-cover"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-active:opacity-100 transition-opacity">
                        <div className="absolute bottom-2 left-2 right-2 flex items-center justify-between">
                          <div className="flex items-center gap-1 text-xs">
                            <Heart className="w-3 h-3 text-pink-400" />
                            {item.likes}
                          </div>
                          <div className="text-xs opacity-60">
                            {CARICATURE_STYLES.find(s => s.id === item.style)?.icon}
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>
            )}
            
            {history.length > 0 && (
              <button
                onClick={() => {
                  if (confirm('Очистить всю историю?')) {
                    setHistory([]);
                  }
                }}
                className="w-full mt-4 py-3 bg-red-500/20 border border-red-500/30 rounded-xl text-red-300 text-sm"
              >
                Очистить историю
              </button>
            )}
          </div>
        )}

        {/* Profile Tab */}
        {activeTab === 'profile' && (
          <div className="px-4 py-4 space-y-4">
            {/* User Profile Card */}
            <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-pink-600/30 to-violet-600/30 p-6 border border-white/10">
              <div className="absolute top-0 right-0 w-32 h-32 bg-pink-500/20 rounded-full blur-3xl" />
              <div className="relative flex items-center gap-4">
                <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-pink-500 to-violet-600 flex items-center justify-center shadow-xl shadow-purple-500/30">
                  <Crown className="w-10 h-10 text-white" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold">{getLevelName(stats.level)}</h2>
                  <p className="text-white/60">Уровень {stats.level}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <Zap className="w-4 h-4 text-amber-400" />
                    <span className="text-amber-400 font-bold">{stats.xp} XP</span>
                  </div>
                </div>
              </div>
              
              {/* XP Progress */}
              <div className="mt-4">
                <div className="flex justify-between text-xs text-white/60 mb-1">
                  <span>Уровень {stats.level}</span>
                  <span>Уровень {stats.level + 1}</span>
                </div>
                <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                  <motion.div 
                    className="h-full bg-gradient-to-r from-amber-500 to-orange-500"
                    style={{ width: `${getXPProgress()}%` }}
                  />
                </div>
              </div>
            </div>
            
            {/* Stats Grid */}
            <div className="grid grid-cols-3 gap-3">
              <div className="p-4 bg-white/5 rounded-2xl border border-white/10 text-center">
                <div className="text-3xl font-bold text-pink-400">{stats.totalCreated}</div>
                <div className="text-xs text-white/60 mt-1">Создано</div>
              </div>
              <div className="p-4 bg-white/5 rounded-2xl border border-white/10 text-center">
                <div className="text-3xl font-bold text-red-400">{stats.totalLikes}</div>
                <div className="text-xs text-white/60 mt-1">Лайков</div>
              </div>
              <div className="p-4 bg-white/5 rounded-2xl border border-white/10 text-center">
                <div className="text-3xl font-bold text-blue-400">{stats.totalShares}</div>
                <div className="text-xs text-white/60 mt-1">Репостов</div>
              </div>
            </div>
            
            {/* Streak */}
            <div className="p-4 bg-gradient-to-r from-orange-500/20 to-amber-500/20 rounded-2xl border border-orange-500/30 flex items-center gap-4">
              <Flame className="w-10 h-10 text-orange-400" />
              <div>
                <div className="font-bold text-lg">{stats.streak} дней подряд</div>
                <div className="text-sm text-white/60">Серия использования</div>
              </div>
            </div>
            
            {/* Achievements */}
            <div className="space-y-3">
              <h3 className="font-semibold flex items-center gap-2">
                <Trophy className="w-5 h-5 text-amber-400" />
                Достижения
              </h3>
              
              <div className="grid grid-cols-4 gap-2">
                {ACHIEVEMENTS.map((achievement) => {
                  const isUnlocked = stats.achievements.includes(achievement.id);
                  return (
                    <motion.button
                      key={achievement.id}
                      whileTap={{ scale: 0.95 }}
                      className={cn(
                        "p-3 rounded-xl text-center transition-all",
                        isUnlocked 
                          ? "bg-gradient-to-br from-amber-500/30 to-orange-500/30 border border-amber-500/50" 
                          : "bg-white/5 border border-white/10 opacity-50"
                      )}
                    >
                      <div className="text-2xl mb-1">{achievement.icon}</div>
                      <div className="text-[10px] font-medium truncate">{achievement.name}</div>
                    </motion.button>
                  );
                })}
              </div>
            </div>
            
            {/* Info Card */}
            <div className="p-4 bg-white/5 rounded-2xl border border-white/10 space-y-3">
              <div className="flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-purple-400" />
                <h3 className="font-semibold">Как получить XP</h3>
              </div>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div className="flex items-center gap-2 text-white/70">
                  <Sparkles className="w-4 h-4 text-pink-400" />
                  Шарж: +25 XP
                </div>
                <div className="flex items-center gap-2 text-white/70">
                  <Share2 className="w-4 h-4 text-blue-400" />
                  Репост: +15 XP
                </div>
                <div className="flex items-center gap-2 text-white/70">
                  <Heart className="w-4 h-4 text-red-400" />
                  Лайк: +5 XP
                </div>
                <div className="flex items-center gap-2 text-white/70">
                  <Trophy className="w-4 h-4 text-amber-400" />
                  Достижение: +XP
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 bg-black/60 backdrop-blur-xl border-t border-white/10 z-50">
        <div className="flex justify-around py-2 pb-safe">
          <button
            onClick={() => setActiveTab('create')}
            className={cn(
              "flex flex-col items-center py-2 px-6 rounded-xl transition-all",
              activeTab === 'create' 
                ? "text-pink-400 bg-pink-500/10" 
                : "text-white/60"
            )}
          >
            <Wand2 className="w-6 h-6" />
            <span className="text-xs mt-1 font-medium">Создать</span>
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={cn(
              "flex flex-col items-center py-2 px-6 rounded-xl transition-all relative",
              activeTab === 'history' 
                ? "text-pink-400 bg-pink-500/10" 
                : "text-white/60"
            )}
          >
            <History className="w-6 h-6" />
            <span className="text-xs mt-1 font-medium">История</span>
            {history.length > 0 && (
              <span className="absolute top-1 right-4 w-5 h-5 bg-pink-500 rounded-full text-[10px] flex items-center justify-center">
                {history.length > 9 ? '9+' : history.length}
              </span>
            )}
          </button>
          <button
            onClick={() => setActiveTab('profile')}
            className={cn(
              "flex flex-col items-center py-2 px-6 rounded-xl transition-all",
              activeTab === 'profile' 
                ? "text-pink-400 bg-pink-500/10" 
                : "text-white/60"
            )}
          >
            <Trophy className="w-6 h-6" />
            <span className="text-xs mt-1 font-medium">Профиль</span>
          </button>
        </div>
      </nav>

      {/* Tutorial Modal */}
      <AnimatePresence>
        {showTutorial && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/90 backdrop-blur-md z-50 flex items-center justify-center p-6"
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-gradient-to-br from-violet-900 to-purple-950 rounded-3xl p-6 max-w-sm w-full border border-white/20 shadow-2xl"
            >
              <div className="text-center">
                <motion.div 
                  animate={{ rotate: [0, 10, -10, 0] }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                  className="w-20 h-20 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-pink-500 to-violet-600 flex items-center justify-center shadow-xl"
                >
                  <Sparkles className="w-10 h-10 text-white" />
                </motion.div>
                <h2 className="text-2xl font-bold mb-2">ШаржМастер PRO</h2>
                <p className="text-white/70 mb-6 text-sm">
                  Создавайте уникальные шаржи и делитесь ими в соцсетях!
                </p>
                
                <div className="space-y-3 text-left mb-6">
                  {[
                    { icon: Camera, text: 'Загрузите фото из галереи или камеры', color: 'pink' },
                    { icon: Palette, text: 'Выберите стиль из 10 вариантов', color: 'violet' },
                    { icon: MessageSquare, text: 'Добавьте готовую подпись для поста', color: 'blue' },
                    { icon: Share2, text: 'Опубликуйте в ВК или Telegram', color: 'green' },
                  ].map((item, i) => (
                    <motion.div 
                      key={i}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.1 * i }}
                      className="flex items-center gap-3"
                    >
                      <div className={cn(
                        "w-8 h-8 rounded-lg flex items-center justify-center",
                        item.color === 'pink' && "bg-pink-500/20",
                        item.color === 'violet' && "bg-violet-500/20",
                        item.color === 'blue' && "bg-blue-500/20",
                        item.color === 'green' && "bg-green-500/20",
                      )}>
                        <item.icon className={cn(
                          "w-4 h-4",
                          item.color === 'pink' && "text-pink-400",
                          item.color === 'violet' && "text-violet-400",
                          item.color === 'blue' && "text-blue-400",
                          item.color === 'green' && "text-green-400",
                        )} />
                      </div>
                      <span className="text-sm text-white/80">{item.text}</span>
                    </motion.div>
                  ))}
                </div>
                
                <motion.button
                  whileTap={{ scale: 0.95 }}
                  onClick={closeTutorial}
                  className="w-full py-3.5 bg-gradient-to-r from-pink-600 via-purple-600 to-violet-600 rounded-xl font-semibold shadow-lg"
                >
                  Начать! 🚀
                </motion.button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Caption Selection Modal */}
      <AnimatePresence>
        {showCaptionModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-end justify-center"
            onClick={() => setShowCaptionModal(false)}
          >
            <motion.div
              initial={{ y: '100%' }}
              animate={{ y: 0 }}
              exit={{ y: '100%' }}
              className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-t-3xl p-6 w-full max-w-lg max-h-[70vh] overflow-y-auto"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="w-12 h-1 bg-white/30 rounded-full mx-auto mb-4" />
              <h3 className="text-lg font-bold mb-4">Выберите подпись</h3>
              
              <div className="space-y-2">
                {CAPTION_TEMPLATES.map((template) => (
                  <button
                    key={template.id}
                    onClick={() => {
                      const styleName = CARICATURE_STYLES.find(s => s.id === selectedStyle)?.nameRu || selectedStyle;
                      setSelectedCaption(template.text.replace('{style}', styleName));
                      setShowCaptionModal(false);
                    }}
                    className="w-full p-3 bg-white/5 rounded-xl text-left text-sm hover:bg-white/10 transition-colors border border-white/10"
                  >
                    {template.text.replace('{style}', CARICATURE_STYLES.find(s => s.id === selectedStyle)?.nameRu || '')}
                  </button>
                ))}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Frame Selection Modal */}
      <AnimatePresence>
        {showFrameModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-end justify-center"
            onClick={() => setShowFrameModal(false)}
          >
            <motion.div
              initial={{ y: '100%' }}
              animate={{ y: 0 }}
              exit={{ y: '100%' }}
              className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-t-3xl p-6 w-full max-w-lg"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="w-12 h-1 bg-white/30 rounded-full mx-auto mb-4" />
              <h3 className="text-lg font-bold mb-4">Рамка для соцсетей</h3>
              
              <div className="grid grid-cols-3 gap-3">
                {FRAMES.map((frame) => (
                  <button
                    key={frame.id}
                    onClick={() => {
                      setSelectedFrame(frame.id);
                      setShowFrameModal(false);
                    }}
                    className={cn(
                      "p-4 rounded-xl border-2 transition-all flex flex-col items-center gap-2",
                      selectedFrame === frame.id
                        ? "border-pink-500 bg-pink-500/20"
                        : "border-white/10 bg-white/5"
                    )}
                  >
                    <div 
                      className="w-10 h-10 rounded-lg"
                      style={{ 
                        background: frame.id === 'gradient' 
                          ? 'linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3)' 
                          : frame.color 
                      }}
                    />
                    <span className="text-xs">{frame.name}</span>
                  </button>
                ))}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* History Item Detail Modal */}
      <AnimatePresence>
        {selectedHistoryItem && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/90 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setSelectedHistoryItem(null)}
          >
            <motion.div
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.9 }}
              className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-3xl p-4 max-w-sm w-full"
              onClick={(e) => e.stopPropagation()}
            >
              <img 
                src={selectedHistoryItem.caricatureImage} 
                alt="Caricature"
                className="w-full aspect-square object-cover rounded-2xl mb-4"
              />
              
              <div className="flex gap-2">
                <button
                  onClick={() => handleDownload(selectedHistoryItem.caricatureImage)}
                  className="flex-1 py-3 bg-white/10 rounded-xl flex items-center justify-center gap-2"
                >
                  <Download className="w-5 h-5" />
                  Скачать
                </button>
                <button
                  onClick={() => {
                    shareToVK(selectedHistoryItem.caricatureImage);
                    setSelectedHistoryItem(null);
                  }}
                  className="flex-1 py-3 bg-[#4a76a8] rounded-xl flex items-center justify-center gap-2"
                >
                  <Share2 className="w-5 h-5" />
                  ВК
                </button>
                <button
                  onClick={() => handleDeleteFromHistory(selectedHistoryItem.id)}
                  className="py-3 px-4 bg-red-500/20 rounded-xl"
                >
                  <Trash2 className="w-5 h-5 text-red-400" />
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

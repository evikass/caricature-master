import { NextRequest, NextResponse } from 'next/server';
import ZAI from 'z-ai-web-dev-sdk';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { image, style, intensity, addWatermark, addFrame } = body;

    if (!image) {
      return NextResponse.json(
        { error: 'Image is required' },
        { status: 400 }
      );
    }

    const zai = await ZAI.create();

    // Style descriptions for caricature
    const styleDescriptions: Record<string, string> = {
      funny: 'hilarious exaggerated caricature, big head small body, comical expression, cartoon style, vibrant colors, humorous distortion, funny face',
      cartoon: 'colorful cartoon caricature, animated style, bold outlines, expressive features, Disney-like exaggeration, playful, vibrant colors',
      artistic: 'artistic caricature illustration, stylized portrait, creative interpretation, artistic brushstrokes, gallery quality, painterly style',
      comic: 'comic book style caricature, dynamic pose, bold ink lines, vibrant colors, superhero exaggeration, action-oriented, pop art',
      sketch: 'hand-drawn sketch caricature, pencil art style, artistic shading, rough edges, expressive lines, artistic interpretation, graphite style',
      anime: 'anime manga style caricature, big expressive eyes, stylized features, Japanese animation style, cute exaggeration, kawaii',
      realistic: 'subtle realistic caricature, slight exaggeration of features, artistic portrait style, professional illustration, refined details',
      celebrity: 'celebrity caricature style, red carpet glamorous, exaggerated features but elegant, magazine cover style, paparazzi photo',
      chibi: 'chibi kawaii style, super deformed cute character, big head tiny body, adorable expression, pastel colors, super cute',
      grotesque: 'grotesque caricature style, highly exaggerated features, artistic distortion, surreal elements, unique character design',
    };

    const selectedStyle = styleDescriptions[style] || styleDescriptions.funny;
    const intensityLevel = intensity || 50;
    
    const intensityDesc = intensityLevel > 70 
      ? 'heavily exaggerated' 
      : intensityLevel > 40 
        ? 'moderately exaggerated' 
        : 'subtly exaggerated';
    
    const prompt = `Create a ${selectedStyle} from this photo. ${intensityDesc} features. Focus on the most distinctive facial features while keeping the person recognizable. High quality, detailed, vibrant colors, professional caricature art. ${addWatermark ? 'Clean professional look.' : ''} ${addFrame ? 'Leave some background space.' : ''}`;

    // Generate caricature
    const response = await zai.images.generations.create({
      prompt: prompt,
      size: '1024x1024',
    });

    const caricatureBase64 = response.data[0]?.base64;

    if (!caricatureBase64) {
      return NextResponse.json(
        { error: 'Failed to generate caricature' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      image: caricatureBase64,
    });

  } catch (error: any) {
    console.error('Caricature generation error:', error);
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}

import { NextRequest, NextResponse } from 'next/server';
import ZAI from 'z-ai-web-dev-sdk';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { image, style, intensity, addWatermark } = body;

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

    // Step 1: Analyze the photo using VLM (Vision Language Model)
    let photoDescription = '';
    try {
      const vlmResponse = await zai.chat.completions.create({
        messages: [
          {
            role: 'system',
            content: 'You are a professional portrait analyst. Analyze the photo and describe the person\'s key facial features that would be important for creating a caricature. Focus on: face shape, distinctive features (nose, eyes, ears, chin, hair), expression, and any unique characteristics. Be concise but detailed. Respond in English.'
          },
          {
            role: 'user',
            content: [
              {
                type: 'image_url',
                image_url: {
                  url: `data:image/jpeg;base64,${image}`
                }
              },
              {
                type: 'text',
                text: 'Describe this person\'s facial features for a caricature artist. Focus on distinctive features that should be emphasized.'
              }
            ]
          }
        ],
        max_tokens: 300,
      });
      
      photoDescription = vlmResponse.choices[0]?.message?.content || '';
      console.log('Photo analysis:', photoDescription);
    } catch (vlmError) {
      console.warn('VLM analysis failed, continuing without:', vlmError);
    }

    // Step 2: Generate caricature based on analysis
    const enhancedPrompt = photoDescription
      ? `Create a ${selectedStyle} of a person with these features: ${photoDescription}. ${intensityDesc} caricature style. Keep the person recognizable but artistically stylized. High quality, detailed, vibrant colors, professional caricature art. ${addWatermark ? 'Clean professional look suitable for social media.' : ''}`
      : `Create a ${selectedStyle} from this photo. ${intensityDesc} features. Focus on the most distinctive facial features while keeping the person recognizable. High quality, detailed, vibrant colors, professional caricature art. ${addWatermark ? 'Clean professional look.' : ''}`;

    // Generate caricature
    const response = await zai.images.generations.create({
      prompt: enhancedPrompt,
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
      analysis: photoDescription,
    });

  } catch (error: any) {
    console.error('Caricature generation error:', error);
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}

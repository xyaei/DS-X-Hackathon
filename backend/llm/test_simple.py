# llm/debug_enhanced.py
import os
import sys
from dotenv import load_dotenv

def debug_enhanced_analyzer():
    print("🔍 Debugging Enhanced Analyzer...")
    
    # 1. Check environment loading
    print("\n1. Checking Environment...")
    load_dotenv()
    gemini_key = os.getenv("GEMINI_API_KEY")
    print(f"   GEMINI_API_KEY found: {'Yes' if gemini_key else 'No'}")
    if gemini_key:
        print(f"   Key: {gemini_key[:10]}...{gemini_key[-4:]}")
    
    # 2. Check imports
    print("\n2. Checking Imports...")
    try:
        import google.generativeai as genai
        print("   ✅ google.generativeai imported successfully")
        
        # Test configuration
        try:
            genai.configure(api_key=gemini_key)
            print("   ✅ Gemini configured successfully")
            
            # Test model creation
            try:
                model = genai.GenerativeModel('models/gemini-2.5-flash')
                print("   ✅ Model creation successful")
                
                # Test content generation
                try:
                    response = model.generate_content("Test")
                    print("   ✅ Content generation successful")
                    print(f"   Response: {response.text}")
                    return True
                except Exception as e:
                    print(f"   ❌ Content generation failed: {e}")
                    
            except Exception as e:
                print(f"   ❌ Model creation failed: {e}")
                
        except Exception as e:
            print(f"   ❌ Gemini configuration failed: {e}")
            
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
    
    return False

def test_enhanced_directly():
    print("\n3. Testing Enhanced Analyzer Directly...")
    
    # Import and test the enhanced analyzer
    from enhanced_analyzer import EnhancedCareerAnalyzer
    
    analyzer = EnhancedCareerAnalyzer()
    
    print(f"   AI Client Provider: {analyzer.ai_client.provider}")
    print(f"   AI Client Model: {analyzer.ai_client.model_name}")
    print(f"   AI Client Available: {analyzer.ai_client.client is not None}")
    
    return analyzer.ai_client.client is not None

if __name__ == "__main__":
    print("🚀 Enhanced Analyzer Debug Session")
    print("=" * 50)
    
    env_ok = debug_enhanced_analyzer()
    analyzer_ok = test_enhanced_directly()
    
    print("\n" + "=" * 50)
    if analyzer_ok:
        print("🎉 Enhanced Analyzer is working with Gemini!")
    else:
        print("🔧 Enhanced Analyzer needs fixes")
        if not env_ok:
            print("💡 Environment/Import issues detected above")
from app import launch_app

def main():
    """Launch the Language Proficiency Estimator Gradio app."""
    print("🚀 Starting Language Proficiency Estimator...")
    print("📝 Make sure your GOOGLE_API_KEY is set in credentials.py or as an environment variable")
    print("🌐 The app will be available at: http://localhost:7860")
    launch_app()


if __name__ == "__main__":
    main()

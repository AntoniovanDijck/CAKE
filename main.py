import argparse
from pipelines.ContextAware_Knowledge_Extraction_Pipeline import CAKE

def main():
    parser = argparse.ArgumentParser(description="Run different components of the CAKE pipeline.")
    parser.add_argument("-run", action="store_true", help="Run the knowledge extraction pipeline.")
    parser.add_argument("-eval", action="store_true", help="Evaluate the pipeline.")
    parser.add_argument("-chat", action="store_true", help="Run chatbot with extracted knowledge.")
    parser.add_argument("-run_all", action="store_true", help="Run all components (pipeline, evaluation, chat).")

    args = parser.parse_args()

    video_url = "https://www.youtube.com/watch?v=g4lHxSAyf7M"  # Example video
    cake = CAKE()

    # Check if no arguments were provided, then default to running all
    if not any(vars(args).values()) or args.run_all:
        cake.run_pipeline(video_url)
        cake.evaluate()
        cake.chat()
    else:
        if args.run:
            cake.run_pipeline(video_url)
        if args.eval:
            cake.evaluate()
        if args.chat:
            cake.chat()

if __name__ == "__main__":
    main()
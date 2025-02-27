from pipelines.ContextAware_Knowledge_Extraction_Pipeline import CAKE

def main():
    video_url = "https://www.youtube.com/watch?v=g4lHxSAyf7M" #How the EVAP System Works (car engine)
    CAKE().run(video_url)

if __name__ == "__main__":
    main()


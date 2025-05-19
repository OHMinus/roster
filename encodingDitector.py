from chardet.universaldetector import UniversalDetector

def encordingDItector(filepath):

    with open(filepath, 'rb') as f:  
        detector = UniversalDetector()
        for line in f:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result.get("encoding")
import numpy as np
import matplotlib.pyplot as plt
import cv2

VIDEO = r"C:\Users\Hugh\Videos\4K Video Downloader\Weather Balloon Flight to Stratosphere [Uncut].mp4"

SECOND = 1000.
MINUTE = 60. * SECOND
HOUR = 60. * MINUTE

BIAS = np.linspace(0., 150., 1080)
FONT = cv2.FONT_HERSHEY_SIMPLEX

FROM = make_time(2, 39, 0)
TO   = make_time(2, 42, 12)
STEP = 0.5 * SECOND     # at half-second intervals

def make_time(hours = 0., minutes = 0., seconds = 0.):
    return hours * HOUR + minutes * MINUTE + seconds * SECOND

def frame_gen(vid, from_, to, step = SECOND):
    for t in np.arange(from_, to, step):
        vid.set(cv2.CAP_PROP_POS_MSEC, t)
        success, frame = vid.read()
        if success:
            yield t, frame
        else:
            break
            
def find_peak(col):
    col = col - BIAS
    return np.min(np.where(col == np.max(col)))

def main():
    vid = cv2.VideoCapture(VIDEO)

    frames = 0
    data = []
    # scan to find frames with centered horizon
    for t, f in frame_gen(vid, FROM, TO, STEP):
        # convert to grayscale
        gr = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        
        # grab three columns - left, center, right - 200 px apart
        a = find_peak(gr[:,  760])
        b = find_peak(gr[:,  960])
        c = find_peak(gr[:, 1160])
        
        height = 1. - b / 540.   # offset from center, in [-1. - 1.]
        slope = (a - c) / 400.
        angle = np.degrees(np.arctan(slope))    # angle in [-90 - 90]
        
        # print(f"{t:>8.0f}: {height:>8.6f} {angle:>8.3f}")
        data.append((t, height, angle))
        frames += 1
        
    print(f"{frames} frames processed")
    
    # extract the top 6 closest-to-centered frames
    data.sort(key = lambda row: abs(row[1]))
    for t, height, angle in data[:6]:
        print(f"{t:>8.0f}:   {height:>8.6f} {angle:>8.3f}")
        vid.set(cv2.CAP_PROP_POS_MSEC, t)
        success, frame = vid.read()
        # add timestamp
        h, t = divmod(t, HOUR)
        m, t = divmod(t, MINUTE)
        s    = t / SECOND
        cv2.putText(frame, f'{h:1.0f}:{m:02.0f}:{s:04.1f}', (50, 200), FONT, 2, (200,255,155), 2, cv2.LINE_AA)
        cv2.imshow('frame',frame)
        cv2.waitKey(0)
    
    cv2.destroyAllWindows()
    cv2.waitKey(5)
    
if __name__ == "__main__":
    main()
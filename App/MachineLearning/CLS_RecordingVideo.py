import cv2

def record(name,id):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # captureDevice = camera
    add = 'http://192.168.1.12:8080/video'
    #cam.open(add)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(
        "Assets\\videos\\"+name+"_"+id+".avi",
        fourcc, 20.0, (640, 480))

    while (True):
        ret, frame = cam.read()
        if (ret == True):

            out.write(frame)

            cv2.imshow('output', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cam.release()
    cv2.destroyAllWindows()
    return 'done'
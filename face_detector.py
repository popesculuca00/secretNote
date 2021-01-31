import cv2
from numpy import asarray
import os
from keras_vggface import VGGFace
from keras_vggface.utils import preprocess_input
from scipy.spatial.distance import cosine

class face_analyzer:
    def __init__(self):
        self.face_not_found = 0
        self.model = VGGFace(   model = 'resnet50',
                                include_top = False,
                                input_shape = (224,224,3),
                                pooling = 'avg'
                             )

    def get_face(self, img):
        face_cascade = cv2.CascadeClassifier("cascades\\data\\haarcascade_frontalface_default.xml")
        gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
        coords = face_cascade.detectMultiScale(gray , 1.1 , 4)
        x , y , w , h = coords[0]
        img = img[y:y+h , x:x+w]
        img = cv2.resize(img , (224,224))
        return img

    def find_best_match(self):
        self.scores = {}
        for person in os.listdir("userdata"):
            self.get_cos_dif("userdata" + "\\" + person + "\\" + "userface.jpg")
        mini = 1
        mini_link = ""
        for person in self.scores:
            prs = person.split('\\')[-2]
            print( f"{prs}  -> {self.scores[person]}" )
            if self.scores[person] < mini :
                mini_link = person
                mini = self.scores[person]

        if mini < 0.4 :
            #print(f"User {mini_link} detected")
            return "\\".join(mini_link.split("\\")[:-1])+ "\\" + "text.txt"
        return None

    def get_cos_dif(self , cnt_person):# , imgs ):
        self.face_not_found = 0
        self.ppl = []
        self.ppl.append(cv2.imread(cnt_person))
        self.ppl.append(cv2.imread("auth_pers.jpg"))

        faces = []
        for img in self.ppl:
            faces.append(self.get_face(img))


        faces = asarray(faces , 'float32')

        faces = preprocess_input(faces, version = 2)

        preds = self.model.predict(faces)
        score = cosine(preds[0] , preds[1])
        #print( f"{cnt_person} --> {score}")
        self.scores[cnt_person] = score



if __name__=="__main__":

    a = face_analyzer()
    test1 = cv2.imread("C:\\Users\\Luca\\Desktop\\gad_final\\userdata\\0\\faces\\face0.jpg")
    test2 = cv2.imread("C:\\Users\\Luca\\Desktop\\gad_final\\userdata\\0\\faces\\face1.jpg")

    cap = cv2.VideoCapture(0)
    image = cv2.flip(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB), 1)
    #plt.imsave("C:\\Users\\Luca\\Desktop\\gad_final\\userdata\\0\\faces\\img_cnt.jpg" , image)

    #test3 = cv2.imread("C:\\Users\\Luca\\Desktop\\gad_final\\userdata\\0\\faces\\img_cnt.jpg")
    test3 = image

    print(a.get_cos_dif([test1, test2]))
    print(a.get_cos_dif([test2, test3]))
    print(a.get_cos_dif([test1, test3]))

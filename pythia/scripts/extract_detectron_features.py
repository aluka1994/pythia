import sys

sys.path.append('/home/anandkumar/textvqa/content/detectron2')

from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
import json
import os
import cv2

from pythia.utils.configuration import Configuration


def get_detectron2_prediction(self, im):
    cfg = get_cfg()
    cfg.merge_from_file(
        "/home/anandkumar/textvqa/content/detectron2/configs/COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml")
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
    cfg.MODEL.WEIGHTS = "detectron2://COCO-Detection/faster_rcnn_R_101_FPN_3x/137851257/model_final_f6e8b1.pkl"
    predictor = DefaultPredictor(cfg)

    # Make prediction
    outputs = predictor(im)

    predictions = outputs["instances"].to("cpu")

    boxes = predictions.pred_boxes if predictions.has("pred_boxes") else None
    scores = predictions.scores if predictions.has("scores") else None
    classes = predictions.pred_classes if predictions.has("pred_classes") else None

    metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])
    dict_to_save_json = {}
    dict_to_save_json['boxes'] = boxes
    dict_to_save_json['scores'] = scores
    dict_to_save_json['classes'] = classes
    dict_to_save_json['labels'] = self._create_text_labels(classes, scores,
                                                                     metadata.get("thing_classes", None))

    return dict_to_save_json


def _create_text_labels(self, classes, scores, class_names):
    """
    Args:
        classes (list[int] or None):
        scores (list[float] or None):
        class_names (list[str] or None):

    Returns:
        list[str] or None
    """
    labels_treshold = []
    labels = None
    if classes is not None and class_names is not None and len(class_names) > 1:
        labels = [class_names[i] for i in classes]
    if scores is not None:
        if labels is None:

            labels = ["{:.0f}%".format(s * 100) for s in scores]
        else:
            for i in len(range(scores)):
                if scores[i] > 0:
                    labels_treshold.append(classes[i])

    return labels_treshold

def runForFiles():
    path = os.path.join(
        os.path.abspath(__file__),
        "../../../configs/textvqa/lorra.yml"
    )

    configuration = Configuration(os.path.abspath(path))

    configuration.freeze()

    config = configuration

    imdb_files = config.imdb_files

    print(imdb_files)


    '''
    imdb_file = imdb_files[dataset_type][imdb_file_index]
    imdb_file = _get_absolute_path(imdb_file)
    imdb = ImageDatabase(self.imdb_file)

    dict={}
    dict = get_detectron2_prediction(cv2.imread(file_base_name))
    with open(sample_info['image_id']+'.json', 'w') as fp:
            json.dump(dict, fp,  indent=4)
    '''

runForFiles()

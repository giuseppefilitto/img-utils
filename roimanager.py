from read_roi import read_roi_file
import os
import pydicom
import matplotlib.pyplot as plt
import argparse


def parse_args():

    description = 'Show ROIs of the original images'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--src', dest='src', required=True, type=str,
                        action='store', help='source directory')
    parser.add_argument('--patience', dest='patience', required=True, type=str,
                        action='store', help='Patience name', default='')
    parser.add_argument('--weight', dest='weight', required=True, type=str,
                        action='store', help='weight (i.e. T2 or DWI)', default='T2')

    args = parser.parse_args()

    return args


def main():

    args = parse_args()

    if not os.path.isdir(args.src):
        raise ValueError('Incorrect directory given')

    roi_dir = os.path.join(args.src, args.patience, args.weight + 'ROI')

    ROIs = []
    for item in os.listdir(roi_dir):

        path_to_roi = os.path.join(roi_dir, item)

        roi = read_roi_file(path_to_roi)

        ROIs.append(roi)

    def _dict(dict_list):
        '''

        useful to get true_dict since roi is {name file : true_dict}.

        '''

        true_dict = []

        for i in dict_list:
            _dict = list(i.values())

            for j in _dict:
                keys = j.keys()
                vals = j.values()

                _dict = {key: val for key, val in zip(keys, vals)}
                true_dict.append(_dict)

        return true_dict

    ROIs = _dict(ROIs)
    ROIs = sorted(ROIs, key=lambda d: list(d.values())[-1])  # ordering dictionaries by positions

    for roi in ROIs:
        position = roi['position']
        x = roi['x']
        y = roi['y']

        # to connect first and last point of the ROI
        x.append(x[0])
        y.append(y[0])

        img_dir = os.path.join(args.src, args.patience, args.weight)

        if not os.path.isdir(img_dir):
            img_dir = img_dir + "AX"

            if not os.path.isdir(img_dir):
                img_dir = os.path.join(args.src, args.patience, args.weight)
                img_dir = img_dir + "5mm"

        img_path = os.path.join(img_dir, str(position) + '.dcm')
        img = pydicom.dcmread(img_path).pixel_array

        plt.figure(1)
        plt.clf()
        plt.imshow(img, cmap="gray")
        plt.plot(x, y, color='red', linestyle='dashed', linewidth=1)
        plt.title("slice " + str(position))
        plt.pause(1)


if __name__ == '__main__':

    main()

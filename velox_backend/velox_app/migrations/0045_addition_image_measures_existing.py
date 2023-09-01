"""This script does 2 things:
1. swap values in bones for fields Cannon and Front Pastern
2. rename second field Cannon for Hind Cannon
"""

import math
import json
import logging
from django.db import migrations, models


class AdditionalData:

    def __int__(self):
        self.points = None
        self.pd = 0

    def getDataPoints(self, data):
        """
        Set data points for calculation
        :param data: JSON data .
        Test data  : {'box': {'top': '1', 'left': '1', 'width': '498', 'height': '376'}, 'parts': {'0': {'x': 61, 'y': 62}, '1': {'x': 230, 'y': 75}, '2': {'x': 196, 'y': 112}, '3': {'x': 167, 'y': 156}, '4': {'x': 201, 'y': 195}, '5': {'x': 203, 'y': 261}, '6': {'x': 203, 'y': 286}, '7': {'x': 202, 'y': 332}, '8': {'x': 187, 'y': 357}, '9': {'x': 357, 'y': 87}, '10': {'x': 430, 'y': 76}, '11': {'x': 453, 'y': 102}, '12': {'x': 433, 'y': 192}, '13': {'x': 391, 'y': 181}, '14': {'x': 454, 'y': 244}, '15': {'x': 429, 'y': 264}, '16': {'x': 451, 'y': 331}, '17': {'x': 433, 'y': 330}, '18': {'x': 437, 'y': 364}, '19': {'x': 420, 'y': 356}}}
        box

        """
        self.points = data.get("parts")

    def getSquareDistance(self, xA, yA, xB, yB):
        """
        Get squred distance between two points
        :param xA: x of point A
        :param yA:
        :param xB:
        :param yB:
        :return: squared distnace as float.
        """
        xDiff = xA - xB
        yDiff = yA - yB
        dist = xDiff * xDiff + yDiff * yDiff
        return dist

    def calculateProcrustesDistance(self):
        """

        Calculate Procrustus Distance
        :return:  Procrustus Distance
        """
        tempX = 0
        tempY = 0
        for key in self.points.keys():
            tempX = tempX + self.points.get(key).get("x")
            tempY = tempY + self.points.get(key).get("y")
        meanX = tempX / len(self.points)
        meanY = tempY / len(self.points)

        sumDistance = 0
        for key in self.points.keys():
            sumDistance = sumDistance + self.getSquareDistance(meanX, meanY, self.points.get(key).get("x"),
                                                               self.points.get(key).get("y"))
        self.pd = round(math.sqrt(sumDistance), 2)
        return self.pd

    def getDistancePerCalibration(self, xA, yA, xB, yB):
        """

        :param xA:
        :param yA:
        :param xB:
        :param yB:
        :return: Calibrated distance with procrustes distance
        """

        xDiff = xA - xB
        yDiff = yA - yB
        dist = math.sqrt(xDiff * xDiff + yDiff * yDiff)
        if (self.pd != 0):
            dist = dist / self.pd

        dist = dist * 1000
        return round(dist, 2)

    def calculateAddtionalData(self, startPoint, endPoint):

        """
        Calculate Distance betweeen two points already in array (self.points)
        :param startPoint: Array position of the point
        :param endPoint:  Array position of the point
        :return:  distance between two points.
        """
        startPoint = startPoint - 1
        endPoint = endPoint - 1
        startX = self.points.get(str(startPoint)).get("x")
        startY = self.points.get(str(startPoint)).get("y")
        endX = self.points.get(str(endPoint)).get("x")
        endY = self.points.get(str(endPoint)).get("y")
        distance = self.getDistancePerCalibration(startX, startY, endX, endY)
        return distance

    def calculateDistance(self, startX, startY, endX, endY):
        return self.getDistancePerCalibration(startX, startY, endX, endY)

    def getIschium(self):
        # Calculate Ischium
        top_tail_x = self.points.get("10").get("x")
        top_tail_y = self.points.get("10").get("y")

        ix = (self.points["12"].get("x") + self.points.get("13").get("x")) / 2
        iy = (self.points["13"].get("x") + self.points.get("14").get("x")) / 2
        isch_imaginary_x = self.points.get("11").get("x") - 100
        isch_imaginary_y = self.points.get("11").get("y")

        isch_temp_x = self.points.get("11").get("x")
        isch_temp_y = self.points.get("11").get("y")

        ischium_x, ischium_y = self.checkLineIntersection(isch_temp_x, isch_temp_y, isch_imaginary_x, isch_imaginary_y,
                                                          top_tail_x, top_tail_y, ix, iy)

        return round(ischium_x, 2), round(ischium_y, 2)

    def checkLineIntersection(self, line1StartX, line1StartY, line1EndX, line1EndY, line2StartX, line2StartY, line2EndX,
                              line2EndY):
        # if the linesintersect, theresultcontainsthex and yoftheintersection(treatingthe lines as infinite) and booleans for whether line segment 1 or line segment 2 contain the point

        denominator = (line2EndY - line2StartY) * (line1EndX - line1StartX) - (line2EndX - line2StartX) * (
                line1EndY - line1StartY);
        if (denominator == 0):
            return None
        a = line1StartY - line2StartY
        b = line1StartX - line2StartX
        numerator1 = (line2EndX - line2StartX) * a - (line2EndY - line2StartY) * b
        numerator2 = (line1EndX - line1StartX) * a - (line1EndY - line1StartY) * b
        a = numerator1 / denominator
        b = numerator2 / denominator

        # if we cast these lines infinitely in both directions, they intersect here:
        x = line1StartX + a * (line1EndX - line1StartX)
        y = line1StartY + a * (line1EndY - line1StartY)

        return x, y

    def getAddtionalData(self):
        """
        The data returned from this class are first calculated and then rounded to first two decimal places. The addional data calculated
        and returned in same sequence as it is mentioned in the return statement below.

        :return: leg_length, fore_limb_length,hind_limb_length, neck_leg_ratio, forelimb_hindlimb_ratio, leg_backlenght_ratio, body_hindlimb_ratio)
        """

        # Get Leg distance
        distance5to8 = self.calculateAddtionalData(5, 8)
        distance8to9 = self.calculateAddtionalData(8, 9)
        leg = round((distance5to8 + distance8to9), 2)

        # Get foreLimbLen
        distance2to4 = self.calculateAddtionalData(2, 4)
        distance4to5 = self.calculateAddtionalData(4, 5)
        forelimbLen = round((distance2to4 + distance4to5 + distance5to8 + distance8to9), 2)

        # Get Ischium 21
        ix, iy = self.getIschium()

        tenx = self.points.get("9").get("x")
        teny = self.points.get("9").get("y")

        distnace10to21 = self.calculateDistance(tenx, teny, ix, iy)

        # Get Femur points 22
        fx = (self.points["12"].get("x") + self.points.get("13").get("x")) / 2
        fy = (self.points["12"].get("y") + self.points.get("13").get("y")) / 2
        distnace21to22 = self.calculateDistance(ix, iy, fx, fy)

        # Get Hock points 23
        hx = (self.points["14"].get("x") + self.points.get("15").get("x")) / 2
        hy = (self.points["14"].get("y") + self.points.get("15").get("y")) / 2
        distanc22to23 = self.calculateDistance(fx, fy, hx, hy)

        # Get Fetlock points 24
        flx = (self.points["16"].get("x") + self.points.get("17").get("x")) / 2
        fly = (self.points["16"].get("y") + self.points.get("17").get("y")) / 2
        distnace23to24 = self.calculateDistance(hx, hy, flx, fly)

        # Get Foot points 25
        ftx = (self.points["18"].get("x") + self.points.get("19").get("x")) / 2
        fty = (self.points["18"].get("y") + self.points.get("19").get("y")) / 2
        distnace24to25 = self.calculateDistance(flx, fly, ftx, fty)

        # Hindlimblength = "10 to 21" + "21 to 22" + "22 to 23" + "23 to 24" + "24 to 25"
        hindlimblength = distnace10to21 + distnace21to22 + distanc22to23 + distnace23to24 + distnace24to25

        neckLenght = self.calculateAddtionalData(1, 2)
        neck_leg_ratio = neckLenght / leg
        forelim_hindlimb_ratio = forelimbLen / hindlimblength

        backlength = self.calculateAddtionalData(2, 10)
        leg_backlenght_ratio = leg / backlength

        bodylength = self.calculateAddtionalData(3, 12)
        body_hindlimb_ratio = bodylength / hindlimblength
        return leg, forelimbLen, round(hindlimblength, 2), round(neck_leg_ratio, 2), round(forelim_hindlimb_ratio,
                                                                                           2), round(
            leg_backlenght_ratio, 2), round(body_hindlimb_ratio, 2)

    def run(self, data: list):
        """
        :param data: list of dict containing edited_landmarks from calculated data column
        :return:  leg, forelimbLen, hindlimblength, neck_leg_ratio, forelim_hindlimb_ratio, leg_backlenght_ratio, body_hindlimb_ratio in this order.
        """
        counter = 0
        newData = {}
        for item in data:
            newData.update({str(counter): {"x": item.get("x"), "y": item.get("y")}})
            counter = counter + 1
        data = {"parts": newData}
        self.getDataPoints(data)
        pd = self.calculateProcrustesDistance()
        self.getIschium()

        return self.getAddtionalData()


def update_image_measurements(apps, schema_editor):
    """set cardio_type for all relevant Measures"""
    logging.info('starting migration')
    ImageMeasurement = apps.get_model('velox_app', 'ImageMeasurement')
    measures = ImageMeasurement.objects.all()
    for measure in measures:
        calculated_data = measure.calculated_data
        if not calculated_data:
            continue

        parts = calculated_data['edited_landmarks']
        ad = AdditionalData()
        leg_length, forelimb_length, hind_length_distance, neck_length_ratio, forelimb_hind_ratio, leg_back_ratio, body_hind_ratio = ad.run(
            parts)
        bones = calculated_data['bones']
        new_data = {
            'Leg Length': {'distance': leg_length, "pointA": "5", "pointB": "9", 'field_name': "leg_length"},
            'Forelimb Length': {'distance': forelimb_length, "pointA": "2", "pointB": "5",
                                'field_name': 'forelimb_length'},
            'Hindlimb Length': {'distance': hind_length_distance, "pointA": "10", "pointB": "25",
                                'field_name': 'hind_length_distance'},
            'Neck/Leg Ratio': {'distance': neck_length_ratio, "pointA": "", "pointB": "",
                               'field_name': 'neck_length_ratio'},
            'Forelimb/Hindlimb Ratio': {'distance': forelimb_hind_ratio, "pointA": "", "pointB": "",
                                        'field_name': 'forelimb_hind_ratio'},
            'Leg/Backlength Ratio': {'distance': leg_back_ratio, "pointA": "", "pointB": "",
                                     'field_name': 'leg_back_ratio'},
            'Bodylength/Hindlimb Ratio': {'distance': body_hind_ratio, "pointA": "", "pointB": "",
                                          'field_name': 'body_hind_ratio'}
        }
        for bone_name in new_data:
            updated = False
            new_bone_data = new_data[bone_name]
            for i, bone_data in enumerate(bones):  # update in case values exist
                if bone_data['boneName'] == bone_name:
                    updated = True
                    bone_data['pointA'] = new_bone_data['pointA']
                    bone_data['pointB'] = new_bone_data['pointB']
                    bone_data['distance'] = new_bone_data['distance']
                bones[i] = bone_data

            if not updated:  # create new item in the list
                bone_data = dict()
                bone_data['pointA'] = new_bone_data['pointA']
                bone_data['pointB'] = new_bone_data['pointB']
                bone_data['distance'] = new_bone_data['distance']
                bone_data['boneName'] = bone_name
                bones.append(bone_data)

            bone_field_name = new_bone_data['field_name']
            setattr(measure, bone_field_name, new_bone_data['distance'])

        calculated_data['bones'] = bones
        measure.calculated_data = calculated_data
        measure.save()
        logging.info(
            f"updating ImageMeasurement {measure.id}\nold data: {calculated_data}\nnew data: {calculated_data} \n")
    logging.info('migration completed')


class Migration(migrations.Migration):
    dependencies = [
        ('velox_app', '0044_auto_20230519_2228'),
    ]

    operations = [
        migrations.RunPython(update_image_measurements, migrations.RunPython.noop)
    ]

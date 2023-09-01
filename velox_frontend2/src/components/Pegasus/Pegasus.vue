<template>
  <section>
    <div ref="container" class="container" style="">
      <div class="row" style="text-align:center">
        <div class="col-sm-12" style="text-align:center">
          <div style="display:inline-block;">
            <div
              id="image-container"
              style="position: relative;width: 498px;height:398px"
            >
              <div class="image">
                <img
                  id="img"
                  ref="image"
                  class="img-thumbnail"
                  :src="previewImgSrc"
                  style="padding:0px;"
                  @click="onImageClick"
                />
                <canvas
                  class="canvas"
                  ref="canvas"
                  width="640"
                  height="640"
                />
              </div>
              <canvas
                class="canvas"
                ref="canvas2"
                width="500"
                height="400"
                />

            </div>
          </div>
          <div class="mt-2">Procrustes Distance : {{ calibrationDist }}</div>

          <div class="mt-2">
            <input
              type="file"
              name="photo"
              ref="add_img_file"
              hidden
              @change="onAddImageChange"
            />
            <button
              class="btn btn-outline-primary "
              id="add_image"
              @click="onAddImageClick"
            >
              Load Image
            </button>
            <button
              class="btn btn-outline-primary"
              id="detect_image"
              @click="onDetectImage"
              :disabled="isDetectDisabled"
            >
              Detect Image
            </button>
            <button
              class="btn btn-outline-primary"
              id="resize_image"
              :disabled="isResizeDisabled"
              @click="resizeImage"
            >
              Crop Image
            </button>
            <button
              class="btn btn-outline-primary"
              id="run_morph"
              @click="runMorph"
              :disabled="isMorphDisabled"
            >
              Run Morph
            </button>
            <!--
            <button
              class="btn btn-outline-primary"
              id="reset_point"
              @click="resetPoint"
            >
              Reset
            </button>
            -->
            <button
              class="btn btn-outline-primary"
              id="save_data"
              :disabled="isSaveDisabled"
              @click="saveData"
            >
              Save
            </button>
            <!--
            <button
              class="btn btn-outline-primary"
              id="add_data"
              @click="showForm('DATA')"
              :disabled="addDataFlag"
            >
              Add Data
            </button>
            -->
          </div>
        </div>
        <!-- <div class="col-sm-1"></div>-->
      </div>

      <div class="row">
        <div class="col-sm-6">
          <div id="addDataFrom" name="addDataFrom" v-if="addData">
            <fieldset class="border p-2  mt-4 mb-4">
              <legend class="w-auto">{{ type }}</legend>
              <div class="col-sm-12">
                <label class="">Name</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="name"
                  name="hname"
                  required
                />
              </div>
              <div class="col-sm-12 mt-2">
                <!-- <h5>Elite :</h5> -->
                <label class="">Elite :</label>
              </div>
              <div class="col-sm-12">
                <label class="radio-inline col-sm-3"
                  ><input
                    type="radio"
                    v-model="elite"
                    name="elite"
                    value="default"
                    checked
                  />
                  Unknown</label
                >
                <label class="radio-inline col-sm-3"
                  ><input
                    type="radio"
                    v-model="elite"
                    name="elite"
                    value="yes"
                  />
                  Yes</label
                >
                <label class="radio-inline col-sm-3"
                  ><input
                    type="radio"
                    v-model="elite"
                    name="elite"
                    value="no"
                  />
                  No</label
                >
              </div>
              <div class="col-sm-12 mt-2 mb-2">
                <!--   type="submit"-->
                <button
                  class="btn btn-outline-primary"
                  @click="submitData"
                  :disabled="!isAddDataFromValid"
                >
                  Submit
                </button>
              </div>
            </fieldset>
          </div>
        </div>
      </div>
    </div>
    <div class="container mt-4">
      <div class="row">
        <div class="col-sm-4 mb-4">
          <table class="table-bordered" style="width: 100%;">
            <thead>
              <tr>
                <th>Marker No</th>
                <th>Marker Name</th>
                <th>X Value</th>
                <th>Y Value</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(m, index) in markerArray"
                :key="`market-array-${index}`"
              >
                <td>{{ index + 1 }}</td>
                <td>{{ m.name }}</td>
                <td>{{ m.x }}</td>
                <td>{{ m.y }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="col-sm-3 mb-4" v-if="bonesData.length > 0">
          <table class="table-bordered" style="width: 100%;">
            <thead>
              <tr>
                <th>Bone Name</th>
                <th>Distance</th>
                <!-- <th>after divide PD</th> -->
              </tr>
            </thead>
            <tbody>
              <tr v-for="(bone, index) in bonesData" :key="`bone-${index}`">
                <td>{{ bone.boneName }}</td>
                <td>{{ bone.distance }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="col-sm-3 mb-4" v-if="angleData.length > 0">
          <table class="table-bordered" style="width: 100%;">
            <thead>
              <tr>
                <th>Angle Name</th>
                <th>Angle (In Deg.)</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(angle, index) in angleData"
                :key="`angle-data-${index}`"
              >
                <td>{{ angle.angleName }}</td>
                <td>{{ angle.angle }}</td>
              </tr>
            </tbody>
          </table>
          <table class="table-bordered mt-4" style="width: 100%;">
            <thead>
              <tr>
                <th>Factor Name</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in factors" :key="`factors-${index}`">
                <td>{{ item.factorName }}</td>
                <td>{{ item.value }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
window.$ = require("jquery");
window.$ = $.extend(require("../../../node_modules/jquery-ui-dist/jquery-ui"));

import { clearBoxes } from "../../utils/renderBox";
import { InferenceSession, Tensor } from "onnxruntime-web";
import { detectImage, resize, download } from "../../utils/detect";

const host = window.location.origin;

var checkFrontPresent = [1, 2, 5, 8, 9, 10, 11];
var checkPresent = [9, 10, 11, 13, 15, 17, 19];
export default {
  props: {
    morphData: { type: Object, default: () => {} }
  },
  data() {
    return {
      boneNames: [
        "Neck",
        "Shoulder",
        "Humerus",
        "Forelimb",
        "Cannon",
        "Front Pastern",
        "Backlength",
        "Bodylength",
        "Pelvis",
        "Femur",
        "Tibia",
        "HindCannon",
        "Fetlock",
        "Pelvis-Femur",
        "Ischium-Hock",
        "Leg Length",
        "Forelimb Length",
        "Hindlimb Length",
        "Neck/Leg Ratio",
        "Forelimb/Hindlimb Ratio",
        "Leg/Backlength Ratio",
        "Bodylength/Hindlimb Ratio"
      ],
      markerArray: [
        { name: "Eye", x: "", y: "", id: "" },
        { name: "Withers", x: "", y: "", id: "" },
        { name: "Midshoulder", x: "", y: "", id: "" },
        { name: "Shoulder", x: "", y: "", id: "" },
        { name: "Top of Leg", x: "", y: "", id: "" },
        { name: "Bottom of Leg", x: "", y: "", id: "" },
        { name: "Top Cannon", x: "", y: "", id: "" },
        { name: "Bottom Cannon", x: "", y: "", id: "" },
        { name: "MidFront Fetlock", x: "", y: "", id: "" },
        { name: "Hip", x: "", y: "", id: "" },
        { name: "Top of Tail", x: "", y: "", id: "" },

        { name: "Point of Ischium", x: "", y: "", id: "" },
        { name: "Caudal Femur", x: "", y: "", id: "" },
        { name: "Frontal Femur", x: "", y: "", id: "" },
        { name: "Caudal Hock", x: "", y: "", id: "" },
        { name: "Frontal Hock", x: "", y: "", id: "" },
        { name: "Caudal Fetlock", x: "", y: "", id: "" },
        { name: "Frontal Fetlock", x: "", y: "", id: "" },
        { name: "Caudal Foot", x: "", y: "", id: "" },
        { name: "Frontal Foot", x: "", y: "", id: "" },
        { name: "Ischium", x: "", y: "", id: "" },
        { name: "Femur", x: "", y: "", id: "" },
        { name: "Hock", x: "", y: "", id: "" },
        { name: "Fetlock", x: "", y: "", id: "" },
        { name: "Foot", x: "", y: "", id: "" }
      ],

      path: process.env.VUE_APP_STATIC_GCS_BUCKET,
      modelName: "yolov8n.onnx",
      modelInputShape: [1, 3, 640, 640],
      resultImageShape: [1, 3, 500, 400],
      topk: 100,
      iouThreshold: 0.45,
      scoreThreshold: 0.2,
      session: {},

      markerArrayCopy: [],
      angleNames: [
        "Shoulder Horizontal",
        "Shoulder Angle",
        "Forearm Angle",
        "Fetlock Angle",
        "Pelvis Horizontal",
        "Hip Angle",
        "Femur Angle",
        "Hock Angle",
        "Hind Fetlock Angle"
      ],
      name: "",
      filename: "",
      array: [],
      generatePoints: [],
      bonesDistance: [],
      boneAngles: [],
      count: 1,
      sex: "1",
      age: "1",
      elite: "default",
      coplanatiry: "1",
      calibrationFlag: true,
      addDataFlag: true,
      isDetectDisabled: true,
      isResizeDisabled: true,
      isMorphDisabled: true,
      isSaveDisabled: true,
      calibrationDist: 0,
      type: "",
      bonesData: {},
      angleData: {},
      calibration: [],
      calibrationDist: 0,
      c1: 0,
      c2: 0,
      factors: [],
      isAddDataFromValid: true,
      isConfirmModalDisabled: false,
      addData: false,
      previewImgSrc: "",
      markerAppData: {},
      imageOffset: {
        left: 0,
        top: 0
      }
    };
  },
  created() {
    let info = this.$cv.getBuildInformation();
    console.log("main created", info, this.$cv);
    this.$cv.onRuntimeInitialized = async () => {
      const [yolov8, nms] = await Promise.all([
        InferenceSession.create(`${this.path}/model/${this.modelName}`),
        InferenceSession.create(`${this.path}/model/nms-yolov8.onnx`),
      ]);
      this.net = yolov8;
      this.nms = nms;

      // warmup main model
      const tensor = new Tensor(
        "float32",
        new Float32Array(this.modelInputShape.reduce((a, b) => a * b)),
        this.modelInputShape
      );
      await yolov8.run({ images: tensor });
      this.session = { net: yolov8, nms: nms };
    };
    this.$cv.onRuntimeInitialized();
  },
  mounted() {
    this.previewImgSrc = require("@/assets/img/pegasus_placeholder.png");
    this.markerArrayCopy = JSON.parse(JSON.stringify(this.markerArray));
  },
  methods: {
    showForm(type) {
      this.addData = true;
      if (type == "PREDICTION") {
        this.type = "Prediction";
      } else {
        this.type = "Add Data";
      }

      this.generateBonePoints();
      this.calculateDistance();
      this.calculateAngles();
      this.drawLines(2);
    },
    onAddImageClick(e) {
      e.preventDefault();

      this.$refs.add_img_file.click();
    },
    onAddImageChange(e) {
      this.previewFile(e.target);
    },

    previewFile(input) {
      this.resetPoint();
      this.calibrationFlag = false;

      var file = input.files[0];

      if (file) {
        this.filename = file.name;
        console.log("file", this.filename);
        var reader = new FileReader();
        let that = this;
        reader.onload = function(e) {
          that.previewImgSrc = e.target.result;
        };
        reader.readAsDataURL(file);
        this.isDetectDisabled = false;
        this.isResizeDisabled = true;
        this.isMorphDisabled = true;
        this.$refs.image.style.height = "100%";

        this.$emit("image-selected", file);
        clearBoxes(this.$refs.canvas);
      }
    },

    onDetectImage(e) {
      e.preventDefault();
      this.isResizeDisabled = false;
      detectImage(
        this.$refs.image,
        this.$refs.canvas,
        this.session,
        this.topk,
        this.iouThreshold,
        this.scoreThreshold,
        this.modelInputShape
      );
      this.isDetectDisabled = true;
    },
    resizeImage(e) {
      e.preventDefault();
      clearBoxes(this.$refs.canvas);
      const url = resize(this.$refs.canvas2, this.$refs.image);
      const file = this.dataURLtoFile(url, this.filename);
      this.$emit("image-selected", file);
      this.isMorphDisabled = false;
      this.isResizeDisabled = true;
    },
    dataURLtoFile(dataurl, filename) {
      var arr = dataurl.split(','),
        mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[arr.length - 1]), 
        n = bstr.length, 
        u8arr = new Uint8Array(n);
      while(n--){
        u8arr[n] = bstr.charCodeAt(n);
      }
      return new File([u8arr], filename, {type:mime});
    },
    resetPoint(e) {
      if (e) e.preventDefault();
      this.bonesData = {};
      this.angleData = {};
      this.calibration = [];
      this.calibrationDist = 0;
      this.c1 = 0;
      this.c2 = 0;
      this.array = [];
      this.count = 1;

      this.markerArray = JSON.parse(JSON.stringify(this.markerArrayCopy));

      this.addDataFlag = true;
      this.isMorphDisabled = false;
      this.isDetectDisabled = true;
      this.isResizeDisabled = true;
      this.isSaveDisabled = true;
      this.calibrationFlag = true;
      this.addData = false;

      $("div").remove(".line_marker");
      $("div").remove(".marker");
      $("div").remove(".ischium_marker");
      $("div").remove(".calibration_marker");

      this.$emit("reset");
    },

    onImageClick(event) {
      this.imageOffset.left = Math.round($("#img").offset().left);
      this.imageOffset.top = Math.round($("#img").offset().top);

      var x = event.pageX - this.imageOffset.left;
      var y = event.pageY - this.imageOffset.top;

      console.log("x,y:", x, y);

      if (this.count <= 20) {
        $("#image-container").append(
          $(
            '<div class="marker ui-draggable ui-draggable-handle" title=' +
              "'" +
              this.markerArray[this.count - 1].name +
              "'" +
              '><span style="color: #ffffff;position: absolute;left: -2px;top: -18px;">' +
              this.count +
              "</span></div>"
          )
            .css({
              position: "absolute",
              top: y + "px",
              left: x + "px",
              //top: event.pageY + "px",
              //left: event.pageX + "px",
              width: "5px",
              height: "5px",
              cursor: "move",
              background: "#7877e6",
              "border-radius": "5px"
            })
            .draggable({ drag: this.onDrag })
        );
        this.array.push({ x: x, y: y, id: this.count });
        this.markerArray[this.count - 1].id = this.count;
        this.markerArray[this.count - 1].x = x;
        this.markerArray[this.count - 1].y = y;

        this.count = this.count + 1;
        if (this.count > 20) {
          this.addDataFlag = false;
          //this.isMorphDisabled = false;
        }
      }
    },

    onDrag(event, id) {
      this.imageOffset.left = Math.round($("#img").offset().left);
      this.imageOffset.top = Math.round($("#img").offset().top);
      let that = this;
      this.markerArray.forEach(value => {
        if (value.id == id.helper[0].innerText) {
          value.x = event.pageX - that.imageOffset.left;
          value.y = event.pageY - that.imageOffset.top;
        }
      });

      this.array.forEach(function(item) {
        if (item.id == id.helper[0].innerText) {
          item.x = event.pageX - that.imageOffset.left;
          item.y = event.pageY - that.imageOffset.top;
          return;
        }
      });

      if (this.array.length >= 20) {
        this.generateBonePoints();
        this.calculateDistance();
        this.calculateAngles();
        this.drawLines(2);
      }

      this.isSaveDisabled = false;
    },
    calculateFactors() {
      var C2, D2, E2, C;
      this.bonesData.forEach(value => {
        //console.log(key + ':----------- ' + value);
        if (value.boneName == "Tibia") {
          E2 = parseFloat(value.distance);
        } else if (value.boneName == "Cannon") {
          C = parseFloat(value.distance);
        } else if (value.boneName == "Pelvis") {
          C2 = parseFloat(value.distance);
        } else if (value.boneName == "Femur") {
          D2 = parseFloat(value.distance);
        }
      });
      var thrust = ((E2 - C) / E2) * 100;
      var O2 =
        C2 * 0.98 > D2 && C2 * 0.98 > E2
          ? "LONG PELVIS"
          : C2 * 1.02 < D2 && C2 * 1.02 < E2
          ? "SHORT PELVIS"
          : D2 * 0.98 > C2 && D2 * 0.98 > E2
          ? "LONG FEMUR"
          : D2 * 1.02 < C2 && D2 * 1.02 < E2
          ? "SHORT FEMUR"
          : E2 * 0.98 > D2 && E2 * 0.98 > C2
          ? "LONG TIBIA"
          : E2 * 1.02 < D2 && E2 * 1.02 < C2
          ? "SHORT TIBIA"
          : "BALANCED";
      var imblance =
        O2 === "BALANCED"
          ? 0
          : O2 == "LONG FEMUR"
          ? D2 - (C2 + E2) / 2
          : O2 == "LONG PELVIS"
          ? C2 - (D2 + E2) / 2
          : O2 == "LONG TIBIA"
          ? E2 - (D2 + C2) / 2
          : O2 == "SHORT FEMUR"
          ? (E2 + C2) / 2 - D2
          : O2 == "SHORT PELVIS"
          ? (E2 + D2) / 2 - C2
          : O2 == "SHORT TIBIA"
          ? (C2 + D2) / 2 - E2
          : -1;

      var f = [];
      f.push({ factorName: "Triangle", value: O2 });
      f.push({ factorName: "Imblance", value: imblance.toFixed(2) });
      f.push({ factorName: "Thrust", value: thrust.toFixed(2) });
      this.factors = f;
    },
    drawLines(thickness) {
      for (var i = 19; i < this.markerArray.length - 1; i++) {
        var x1 = parseFloat(this.markerArray[i].x);
        var y1 = parseFloat(this.markerArray[i].y);
        var x2 = parseFloat(this.markerArray[i + 1].x);
        var y2 = parseFloat(this.markerArray[i + 1].y);
        if (i == 19) {
          x1 = parseFloat(this.array[9].x);
          y1 = parseFloat(this.array[9].y);
          x2 = parseFloat(this.markerArray[20].x);
          y2 = parseFloat(this.markerArray[20].y);
        }
        // distance
        var length = Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
        // center
        var cx = (x1 + x2) / 2 - length / 2 + 2;
        var cy = (y1 + y2) / 2 - thickness / 2 + 2;
        // angle
        var angle = Math.atan2(y1 - y2, x1 - x2) * (180 / Math.PI);
        // make hr
        $("#image-container").append(
          $(
            '<div class="line_marker ui-draggable ui-draggable-handle" ></div>'
          ).css({
            padding: "0px",
            height: thickness + "px",
            background: "#2ad451",
            "line-height": "1px",
            position: "absolute",
            left: cx + "px",
            top: cy + "px",
            width: length + "px",
            "-moz-transform": "rotate(" + angle + "deg)",
            "-webkit-transform": "rotate(" + angle + "deg)",
            "-o-transform": "rotate(" + angle + "deg)",
            "-ms-transform": "rotate(" + angle + "deg)",
            transform: "rotate(" + angle + "deg)"
          }) //.draggable({ drag: onDrag })
        );
      }
      this.calculateFactors();
    },
    checkLineIntersection(
      line1StartX,
      line1StartY,
      line1EndX,
      line1EndY,
      line2StartX,
      line2StartY,
      line2EndX,
      line2EndY
    ) {
      // if the lines intersect, the result contains the x and y of the intersection (treating the lines as infinite) and booleans for whether line segment 1 or line segment 2 contain the point
      var denominator, a, b, numerator1, numerator2, result, x, y;
      denominator =
        (line2EndY - line2StartY) * (line1EndX - line1StartX) -
        (line2EndX - line2StartX) * (line1EndY - line1StartY);
      if (denominator == 0) {
        return result;
      }
      a = line1StartY - line2StartY;
      b = line1StartX - line2StartX;
      numerator1 =
        (line2EndX - line2StartX) * a - (line2EndY - line2StartY) * b;
      numerator2 =
        (line1EndX - line1StartX) * a - (line1EndY - line1StartY) * b;
      a = numerator1 / denominator;
      b = numerator2 / denominator;

      // if we cast these lines infinitely in both directions, they intersect here:
      x = line1StartX + a * (line1EndX - line1StartX);
      y = line1StartY + a * (line1EndY - line1StartY);

      return { x: x, y: y };
    },
    getSquareDistance(xA, yA, xB, yB) {
      var xDiff = xA - xB;
      var yDiff = yA - yB;
      //var dist=Math.sqrt(xDiff * xDiff + yDiff * yDiff);
      var dist = xDiff * xDiff + yDiff * yDiff;
      return dist;
    },
    getDistancePerCalibration(xA, yA, xB, yB) {
      var xDiff = xA - xB;
      var yDiff = yA - yB;
      var dist = Math.sqrt(xDiff * xDiff + yDiff * yDiff);
      if (this.calibrationDist != 0) {
        dist = dist / this.calibrationDist;
      }
      dist = dist * 1000;
      return dist.toFixed(2);
    },
    getOtherDistancePerCalibration(xA, xB) {
      var xDiff = xA - xB;
      var dist = Math.sqrt(xDiff * xDiff);
      if (this.calibrationDist != 0) {
        dist = dist / this.calibrationDist;
      }
      dist = dist * 1000;
      return dist.toFixed(2);
    },
    calculateProcrustesDistance() {
      var tempX = 0;
      var tempY = 0;
      this.array.forEach(function(item) {
        tempX = tempX + item.x;
        tempY = tempY + item.y;
      });
      var meanX = tempX / this.array.length;
      var meanY = tempY / this.array.length;
      this.c1 = meanX.toFixed(2);
      this.c2 = meanY.toFixed(2);

      var sumDistance = 0;
      let that = this;
      this.array.forEach(function(item) {
        sumDistance =
          sumDistance + that.getSquareDistance(meanX, meanY, item.x, item.y);
      });
      return Math.sqrt(sumDistance).toFixed(2);
    },

    generateBonePoints() {
      if (this.array.length >= 2) {
        var pntCnt = 20;
        this.generatePoints = [];
        $("div").remove(".ischium_marker");
        $("div").remove(".line_marker");
        this.calibrationDist = this.calculateProcrustesDistance();
        let that = this;
        this.array.forEach(function(item, i) {
          //console.log("pint---", i)
          if (i == that.array.length - 1) {
            return;
          }
          if (i > 10 && !checkPresent.includes(i)) {
            var x = (that.array[i].x + that.array[i + 1].x) / 2;
            var y = (that.array[i].y + that.array[i + 1].y) / 2;
            that.generatePoints.push({ x: x, y: y, id: pntCnt });
            that.markerArray[pntCnt].x = x;
            that.markerArray[pntCnt].y = y;
            pntCnt += 1;
            $("#image-container").append(
              $(
                '<div class="ischium_marker ui-draggable ui-draggable-handle" title="Ischium"><span style="color: yellow;position: absolute;left: -5px;top: 2px;">' +
                  pntCnt +
                  "</span></div>"
              ).css({
                position: "absolute",
                top: y + "px",
                left: x + "px",
                width: "5px",
                height: "5px",
                cursor: "move",
                background: "yellow",
                "border-radius": "5px"
              })
            );
          } else if (i == 10) {
            var ischTemp = Object.assign({}, that.array[i + 1]);
            var ix = (that.array[12].x + that.array[13].x) / 2;
            var iy = (that.array[13].x + that.array[14].x) / 2;
            var ischium = that.checkLineIntersection(
              ischTemp.x - 100,
              ischTemp.y,
              that.array[i + 1].x,
              that.array[i + 1].y,
              that.array[i].x,
              that.array[i].y,
              ix,
              iy
            );
            that.gischium = ischium;
            if (ischium != undefined) {
              ischium.x = ischium.x.toFixed(2);
              ischium.y = ischium.y.toFixed(2);
              that.generatePoints.push({
                x: ischium.x,
                y: ischium.y,
                id: pntCnt
              });
              that.markerArray[pntCnt].x = ischium.x;
              that.markerArray[pntCnt].y = ischium.y;
            }
            pntCnt += 1;
            $("#image-container").append(
              $(
                '<div class="ischium_marker ui-draggable ui-draggable-handle" title="Ischium"><span style="color:yellow;position: absolute;left: -5px;top: 2px;">21</span></div>'
              ).css({
                position: "absolute",
                top: ischium.y + "px",
                left: ischium.x + "px",
                width: "5px",
                height: "5px",
                cursor: "move",
                background: "yellow",
                "border-radius": "5px"
              })
            );
          }
        });
      }
    },

    calculateFrontBoneDistance() {
      var boneCounter = 0;
      let that = this;
      this.array.forEach(function(item, i) {
        if (i == that.array.length - 1) {
          return;
        }
        if (i < 12 && !checkFrontPresent.includes(i)) {
          var distance = that.getDistancePerCalibration(
            that.array[i].x,
            that.array[i].y,
            that.array[i + 1].x,
            that.array[i + 1].y
          );
          var n = i + 1;
          that.bonesDistance.push({
            pointA: i + 1,
            pointB: n + 1,
            boneName: that.boneNames[boneCounter++],
            distance: distance
          });
        } else if (i == 1) {
          var distance = that.getDistancePerCalibration(
            that.array[1].x,
            that.array[1].y,
            that.array[3].x,
            that.array[3].y
          );
          that.bonesDistance.push({
            pointA: i + 1,
            pointB: 4,
            boneName: that.boneNames[boneCounter++],
            distance: distance
          });
        } else if (i == 9) {
          var distance = that.getDistancePerCalibration(
            that.array[9].x,
            that.array[9].y,
            that.array[1].x,
            that.array[1].y
          );
          that.bonesDistance.push({
            pointA: i + 1,
            pointB: 2,
            boneName: that.boneNames[boneCounter++],
            distance: distance
          });
          that.scapulaToHipDistance = distance;
        } else if (i == 11) {
          var distance = that.getDistancePerCalibration(
            that.array[2].x,
            that.array[2].y,
            that.array[11].x,
            that.array[11].y
          );
          that.bonesDistance.push({
            pointA: i + 1,
            pointB: 3,
            boneName: that.boneNames[boneCounter++],
            distance: distance
          });
          that.midSToBackSDistance = distance;
        }
      });

      if (this.scapulaToHipDistance != 0) {
        var distance = this.getDistancePerCalibration(
          this.array[4].x,
          this.array[4].y,
          this.array[12].x,
          this.array[12].y
        );
        //console.log("here......",distance+" SHDist...."+this.scapulaToHipDistance);
        var distance3 = distance / this.scapulaToHipDistance;
        distance3 = distance3.toFixed(2);
        this.bonesDistance.push({
          pointA: "",
          pointB: "",
          boneName: "Scope",
          distance: distance3
        });
      }
      if (this.midSToBackSDistance != 0) {
        var distance = this.getDistancePerCalibration(
          this.array[1].x,
          this.array[1].y,
          this.array[7].x,
          this.array[1].y
        );
        var distance4 = distance / this.midSToBackSDistance;
        distance4 = distance4.toFixed(2);
        this.bonesDistance.push({
          pointA: "",
          pointB: "",
          boneName: "Proportion",
          distance: distance4
        });
      }
    },
    calculateDistance() {
      var boneCounter = 8;
      var pntlbl = 21;
      this.bonesDistance = [];
      if (this.array.length >= 2) {
        if (this.array[0].x < this.array[1].x) {
          this.orientation = true;
        } else {
          this.orientation = false;
        }
        this.calibrationDist = this.calculateProcrustesDistance();
        this.calculateFrontBoneDistance();
        var distance = this.getDistancePerCalibration(
          this.array[9].x,
          this.array[9].y,
          this.generatePoints[0].x,
          this.generatePoints[0].y
        );
        this.bonesDistance.push({
          pointA: 10,
          pointB: 21,
          boneName: this.boneNames[boneCounter++],
          distance: distance
        });
        let that = this;
        this.generatePoints.forEach(function(item, i) {
          if (i == that.generatePoints.length - 1) {
            return;
          }
          var distance = that.getDistancePerCalibration(
            that.generatePoints[i].x,
            that.generatePoints[i].y,
            that.generatePoints[i + 1].x,
            that.generatePoints[i + 1].y
          );
          var n = pntlbl + i;
          that.bonesDistance.push({
            pointA: n,
            pointB: n + 1,
            boneName: that.boneNames[boneCounter++],
            distance: distance
          });
        });

        var distance1 = this.getOtherDistancePerCalibration(
          this.array[9].x,
          this.generatePoints[1].x
        ); //this.getDistancePerCalibration(this.array[0].x, this.array[0].y, this.generatePoints[1].x, this.generatePoints[1].y);
        this.bonesDistance.push({
          pointA: 10,
          pointB: 22,
          boneName: this.boneNames[boneCounter++],
          distance: distance1
        });

        var distance2 = this.getOtherDistancePerCalibration(
          this.generatePoints[0].x,
          this.generatePoints[2].x
        ); //this.getDistancePerCalibration(this.generatePoints[0].x, this.generatePoints[0].y, this.generatePoints[2].x, this.generatePoints[2].y);
        this.bonesDistance.push({
          pointA: 21,
          pointB: 23,
          boneName: this.boneNames[boneCounter++],
          distance: distance2
        });
        //Adding extra bones
        var distance5to8 = that.getDistancePerCalibration(
          that.array[4].x,
          that.array[4].y,
          that.array[7].x,
          that.array[7].y
        );
        var distance8to9 = that.getDistancePerCalibration(
          that.array[7].x,
          that.array[7].y,
          that.array[8].x,
          that.array[8].y
        );
        var leg = (Number(distance5to8) + Number(distance8to9)).toFixed(2);
        this.bonesDistance.push({
          pointA: 5,
          pointB: 9,
          boneName: this.boneNames[boneCounter++],
          distance: leg
        });
        // console.log("leg length",Number(distance5to8)+Number(distance8to9));

        var distance2to4 = that.getDistancePerCalibration(
          that.array[1].x,
          that.array[1].y,
          that.array[3].x,
          that.array[3].y
        );
        var distance4to5 = that.getDistancePerCalibration(
          that.array[3].x,
          that.array[3].y,
          that.array[4].x,
          that.array[4].y
        );
        var forelimbLen = (
          Number(distance2to4) +
          Number(distance4to5) +
          Number(distance5to8) +
          Number(distance8to9)
        ).toFixed(2);
        this.bonesDistance.push({
          pointA: 2,
          pointB: 5,
          boneName: this.boneNames[boneCounter++],
          distance: forelimbLen
        });
        // console.log("forelimb length",Number(distance2to4)+Number(distance4to5)+Number(distance5to8)+Number(distance8to9));
        var tempHindLenDist = 0;
        this.generatePoints.forEach(function(item, i) {
          if (i == that.generatePoints.length - 1) {
            return;
          }
          var genPtDist = that.getDistancePerCalibration(
            that.generatePoints[i].x,
            that.generatePoints[i].y,
            that.generatePoints[i + 1].x,
            that.generatePoints[i + 1].y
          );
          tempHindLenDist = tempHindLenDist + Number(genPtDist);
        });
        //console.log("tempHindLenDist",tempHindLenDist);
        var hindLenDist = this.getDistancePerCalibration(
          this.array[9].x,
          this.array[9].y,
          this.generatePoints[0].x,
          this.generatePoints[0].y
        );
        // console.log("hindLenDist before",hindLenDist);
        hindLenDist = (tempHindLenDist + Number(hindLenDist)).toFixed(2);
        // console.log("hindLenDist",hindLenDist);
        this.bonesDistance.push({
          pointA: 10,
          pointB: 25,
          boneName: this.boneNames[boneCounter++],
          distance: hindLenDist
        });
        //Calculating ratios
        var neckLegRatio = this.bonesDistance[0].distance / Number(leg);
        neckLegRatio = neckLegRatio.toFixed(2);
        //  console.log("neckLegRatio",neckLegRatio);
        this.bonesDistance.push({
          pointA: "",
          pointB: "",
          boneName: this.boneNames[boneCounter++],
          distance: neckLegRatio
        });
        var foreHimbRatio = forelimbLen / Number(hindLenDist);
        foreHimbRatio = foreHimbRatio.toFixed(2);
        //  console.log("foreHimbRatio",foreHimbRatio);
        this.bonesDistance.push({
          pointA: "",
          pointB: "",
          boneName: this.boneNames[boneCounter++],
          distance: foreHimbRatio
        });
        var legBackRatio = Number(leg) / this.bonesDistance[6].distance;
        legBackRatio = legBackRatio.toFixed(2);
        // console.log("legBackRatio",legBackRatio);
        this.bonesDistance.push({
          pointA: "",
          pointB: "",
          boneName: this.boneNames[boneCounter++],
          distance: legBackRatio
        });
        var bodyHimbRatio =
          this.bonesDistance[7].distance / Number(hindLenDist);
        bodyHimbRatio = bodyHimbRatio.toFixed(2);
        //console.log("bodyHimbRatio",bodyHimbRatio);
        this.bonesDistance.push({
          pointA: "",
          pointB: "",
          boneName: this.boneNames[boneCounter++],
          distance: bodyHimbRatio
        });
        this.bonesData = this.bonesDistance;
      }
    },

    find_angle(A, B, C) {
      var AB = Math.sqrt(Math.pow(B.x - A.x, 2) + Math.pow(B.y - A.y, 2));
      var BC = Math.sqrt(Math.pow(B.x - C.x, 2) + Math.pow(B.y - C.y, 2));
      var AC = Math.sqrt(Math.pow(C.x - A.x, 2) + Math.pow(C.y - A.y, 2));
      var angle =
        Math.acos((BC * BC + AB * AB - AC * AC) / (2 * BC * AB)) *
        (180 / Math.PI);
      return angle.toFixed(0);
    },

    calculateFrontAngles() {
      if (this.array.length >= 2) {
        var boneAngleCounter = 0;
        for (var i = 0; i < 4; i++) {
          switch (i) {
            case 0:
              var temp = Object.assign({}, this.array[3]);
              if (this.orientation) {
                temp.x = temp.x + 50;
              } else {
                temp.x = temp.x - 50;
              }
              var angle = this.find_angle(this.array[1], this.array[3], temp);
              this.boneAngles.push({
                angleName: this.angleNames[boneAngleCounter++],
                angle: angle
              });
              break;
            case 1:
              var angle = this.find_angle(
                this.array[4],
                this.array[3],
                this.array[1]
              );
              this.boneAngles.push({
                angleName: this.angleNames[boneAngleCounter++],
                angle: angle
              });
              break;
            case 2:
              var angle = this.find_angle(
                this.array[3],
                this.array[4],
                this.array[5]
              );
              this.boneAngles.push({
                angleName: this.angleNames[boneAngleCounter++],
                angle: angle
              });
              break;
            case 3:
              var angle = this.find_angle(
                this.array[6],
                this.array[7],
                this.array[8]
              );
              this.boneAngles.push({
                angleName: this.angleNames[boneAngleCounter++],
                angle: angle
              });
              break;
            default:
              break;
          }
        }
      }
    },
    calculateAngles() {
      this.boneAngles = [];
      if (this.array.length >= 2) {
        this.calculateFrontAngles();
        var boneAngleCounter = 4;
        var temp = Object.assign({}, this.gischium);
        temp.x = temp.x - 50;
        if (this.gischium != undefined) {
          var angle = this.find_angle(this.array[9], this.gischium, temp);
          this.boneAngles.push({
            angleName: this.angleNames[boneAngleCounter++],
            angle: angle
          });
        } else {
          boneAngleCounter++;
        }
        let that = this;
        this.generatePoints.forEach(function(item, i) {
          if (i == that.generatePoints.length - 1) {
            return;
          }
          var angle = 0;
          if (i == 0) {
            angle = that.find_angle(
              that.array[9],
              that.generatePoints[i],
              that.generatePoints[i + 1]
            );
          } else {
            angle = that.find_angle(
              that.generatePoints[i - 1],
              that.generatePoints[i],
              that.generatePoints[i + 1]
            );
          }
          that.boneAngles.push({
            angleName: that.angleNames[boneAngleCounter++],
            angle: angle
          });
        });
        that.angleData = that.boneAngles;
      }
    },
    async submitData(e) {
      e.preventDefault();

      let result = await this.$formHelpers.showConfirmation(
        "Commit this data to storage?"
      );

      if (!result) return;

      var appData = [];
      appData.push({ key: "Name", value: this.name });
      appData.push({ key: "PD", value: this.calibrationDist });
      var _elite = "2";
      if (this.elite == "no") {
        _elite = "0";
      }
      if (this.elite == "yes") {
        _elite = "1";
      }
      appData.push({ key: "Elite", value: _elite });
      this.bonesData.forEach(function(item) {
        appData.push({ key: item.boneName, value: item.distance });
      });
      this.angleData.forEach(function(item) {
        appData.push({ key: item.angleName, value: item.angle });
      });
      this.factors.forEach(function(item) {
        appData.push({ key: item.factorName, value: item.value });
      });
      this.markerAppData = {
        data: appData
      };
    },
    runMorph(e) {
      e.preventDefault();
      if (this.array.length >= 20) {
        this.generateBonePoints();
        this.calculateDistance();
        this.calculateAngles();
        this.drawLines(2);
      }
      this.isSaveDisabled = false;
      this.$emit("morph");

      this.isMorphDisabled = true;
    },
    getCalculations() {
      let result = {
        procrustesDistance: this.calibrationDist,
        morph: this.morphData,
        edited_landmarks: this.array,
        bones: this.bonesData,
        angels: this.angleData,
        factors: this.factors
      };

      return result;
    },
    saveData(e) {
      e.preventDefault();
      let result = this.getCalculations();
      this.$emit("save", result);

      this.isSaveDisabled = true;
    }
  },
  watch: {
    morphData(newVal) {
      if (newVal.parts) {
        for (let p in newVal.parts) {
          this.onImageClick({
            pageX:  newVal.parts[p].x + Math.round($("#img").offset().left),
            pageY:  newVal.parts[p].y + Math.round($("#img").offset().top)
          });
        }

        this.generateBonePoints();
        this.calculateDistance();
        this.calculateAngles();
        this.drawLines(2);

        this.isSaveDisabled = false;
      }
    }
  }
};
</script>

<style>
#img {
  width: 100%;
}
.image {
  position: relative;
}
.canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
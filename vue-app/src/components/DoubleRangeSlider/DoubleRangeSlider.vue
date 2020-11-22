<template>
<div class="content">
  <div id="my-slider"
       :se-min="minThreshold"
       :se-step="step"
       :se-min-value="min"
       :se-max-value="max"
       :se-max="maxThreshold"
       class="slider">
    <div class="slider-touch-left">
      <span></span>
    </div>
    <div class="slider-touch-right">
      <span></span>
    </div>
    <div class="slider-line">
      <span></span>
    </div>
  </div>
</div>
</template>

<script>
import ZbRangeSlider from './ZbRangeSlider';

export default {

  props: {
    minThreshold: {
      type: Number,
      default: -100,
    },
    maxThreshold: {
      type: Number,
      default: 100,
    },
    step: {
      type: Number,
      default: 1,
    },
    min: {
      type: Number,
      required: true,
    },
    max: {
      type: Number,
      required: true,
    },
  },

  data() {
    return {
      instance: undefined,
    };
  },

  mounted() {
    this.instance = new ZbRangeSlider('my-slider');
    this.instance.didChanged = (min, max) => this.changed(min, max);
    this.instance.onChange = (min, max) => this.updateValues(min, max);
    this.updateValues(this.min, this.max);
  },

  methods: {
    updateValues(minVal, maxVal) {
      this.$emit('update', { min: minVal, max: maxVal });
    },
    changed(minVal, maxVal) {
      this.$emit('change', { min: minVal, max: maxVal });
    },
  },

  watch: {
    max() {
      this.instance.setMaxThreshold(this.max);
      this.updateValues(this.min, this.max);
    },
    min() {
      this.instance.setMinThreshold(this.min);
      this.updateValues(this.min, this.max);
    },
  },

};

</script>

<style lang="scss">

$primary: #75b239;
$primary-dark: #559930;

.slider {
  display: block;
  position: relative;
  height: 32px;
  width: 100%;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  -o-user-select: none;
  user-select: none;

.slider-touch-left,
.slider-touch-right {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  display: block;
  position: absolute;
  height: 32px;
  width: 32px;
  padding: 6px;
  z-index: 2;
    span {
      display: block;
      width: 100%;
      height: 100%;
      background: $primary;
      border: 1px solid $primary-dark;
      border-radius: 50%;
    }
}
.slider-line {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  position: absolute;
  width: calc(100% - 36px);
  left: 18px;
  top: 13px;
  height: 7px;
  border-radius: 4px;
  background: #f0f0f0;
  z-index: 0;
  overflow: hidden;
  span {
    display: block;
    height: 100%;
    width: 0%;
    background: $primary;
  }
}
}
</style>

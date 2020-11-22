<template>
  <div>
  <b-input-group class="mb-3" style="max-width: 120px;">
    <b-input-group-prepend>
      <b-button variant="outline-primary"
                @click="decrease">
                  &minus;
      </b-button>
    </b-input-group-prepend>
    <b-form-input type="text"
            class="form-control text-center"
            :formatter="formatter"
            :value = "value"
            @change="setValue($event)"
            />
    <b-input-group-append>
      <b-button variant="outline-primary"
                @click="increase">
                  &plus;
      </b-button>
    </b-input-group-append>
  </b-input-group>
</div>
</template>

<script>

export default {

  name: 'NumberSpinner',

  props: {
    min: {
      type: Number,
      required: true,
    },
    max: {
      type: Number,
      required: true,
    },
    value: {
      type: Number,
      required: true,
    },
  },

  data() {
    return {
      currentValue: 0,
    };
  },

  methods: {
    increase() {
      let val = (this.value < this.max) ? this.value + 1 : this.max;
      this.$emit('input', val);
    },
    decrease() {
      let val = (this.value > this.min) ? this.value - 1 : this.min;
      this.$emit('input', val);
    },
    setValue(event) {
      console.log(event)
      this.$emit('input', Number(event));
    },
    formatter(value) {
      const val = value;
      const { max } = this;
      const { min } = this;

      if (/\d+/.test(val)) {
        if (Number(val) > max) {
          return max;
        } if (Number(val) < min) {
          return min;
        }
        return val;
      }
      return 0;
    },
  },

};

</script>

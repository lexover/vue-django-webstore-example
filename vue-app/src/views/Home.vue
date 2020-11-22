<template>
  <div>
    <div class="site-block-cover">
      <b-carousel id="title-carousel" :interval="4000" controls background="#ababab">
        <template v-for="(slide, index) in slides" >
        <b-carousel-slide v-bind:key="slide.id" v-bind:img-src="slide.image">
    <b-container>
      <b-row>
        <b-col lg="12" align-self="center" class="mx-auto">
          <h1>{{ slidesTitles[index][0] }}
            <span style="color: #75b239;">{{ slidesTitles[index][1] }}</span>
          </h1>
          <div class="carousel-text"> {{ slide.text }}</div>
          <router-link :to="{name: 'catalog'}">
            <b-button class="carousel-btn">SHOP NOW</b-button>
          </router-link>
        </b-col>
      </b-row>
    </b-container>
        </b-carousel-slide>
      </template>
      </b-carousel>
    </div>
    <div class="site-section py-5">
      <b-container>
        <b-row>
          <feature v-for="feature in features"
                   v-bind:key="feature.id"
                   v-bind:icon-class="feature.iconClass"
                   v-bind:title="feature.title"
                   v-bind:text="feature.text"
                   v-bind:reference="feature.reference">
          </feature>
        </b-row>
      </b-container>
    </div>
  </div>
</template>

<script>

import { BCarousel, BCarouselSlide } from 'bootstrap-vue';
import Feature from '@/components/Feature.vue';

export default {

  name: 'Home',

  components: {
    Feature,
    BCarousel, 
    BCarouselSlide
  },

  data() {
    return {
      features: [
        {
          id: 1,
          iconClass: 'flaticon-24-hours-drugs-delivery',
          title: 'Free Delivery',
          text: 'Lorem error iusto obcaecati voluptate consequuntur'
                + 'Iure vero officiis quos ab veniam tenetur, assumenda?',
          reference: '/',
        },

        {
          id: 2,
          iconClass: 'flaticon-medicine',
          title: 'New Medicine Everyday',
          text: 'Lorem error iusto obcaecati voluptate consequuntur'
                + 'Iure vero officiis quos ab veniam tenetur, assumenda?',
          reference: '/',
        },

        {
          id: 3,
          iconClass: 'flaticon-test-tubes',
          title: 'Medicines Guaranteed',
          text: 'Lorem error iusto obcaecati voluptate consequuntur'
                + 'Iure vero officiis quos ab veniam tenetur, assumenda?',
          reference: '/',
        },
      ],
      slides: [
        {
          id: 1,
          image: require('@/assets/images/hero_bg.jpg'),
          title: 'New Medicine Everyday',
          text: 'Lorem error iusto obcaecati voluptate consequuntur'
                + 'Iure vero officiis quos ab veniam tenetur, assumenda?',
          reference: '#',
        },
        {
          id: 2,
          image: require('@/assets/images/hero_bg_2.jpg'),
          title: 'New Medicine Everyday',
          text: 'Lorem error iusto obcaecati voluptate consequuntur'
                + 'Iure vero officiis quos ab veniam tenetur, assumenda?',
          reference: '#',
        }],
    };
  },

  computed: {
    slidesTitles() {
      return this.slides.map((item) => {
        const last = item.title.split(' ').pop();
        return [item.title.replace(last, ''), last];
      });
    },
  },

};

</script>

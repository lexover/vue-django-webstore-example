import { shallowMount, createLocalVue } from '@vue/test-utils'
import VueRouter from 'vue-router'
import Vuex from 'vuex'
import BootstrapVue from 'bootstrap-vue'
import App from '@/App'

const localVue = createLocalVue()
localVue.use(VueRouter)
localVue.use(Vuex)
const router = new VueRouter()
const store = new Vuex.Store()

localVue.use(BootstrapVue)

describe('App.vue', () => {
  it('has a name', () => {
    expect(App.name).toMatch('app')
  })
  it('is Vue instance', () => {
    const wrapper = shallowMount(App, {
      localVue,
      router,
      store,
    })
    expect(wrapper.vm).toBeTruthy()
  })
  it('is App', () => {
    const wrapper = shallowMount(App, {
      localVue,
      router,
      store
    })
    expect(wrapper.is(App)).toBeTruthy()
  })
})

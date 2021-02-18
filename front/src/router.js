import Vue from 'vue'
import Router from 'vue-router'
import Input from './components/Input'
import Show from './components/show'
import Search from './components/Search'
import LineWidth from './components/LineWidthView'

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'input',
            component: Input
        },
        {
            path: '/show',
            name: 'show',
            component: Show
        },
        {
            path: '/search',
            name: 'search',
            component: Search
        },
        {
            path: '/reserch',
            name: 'reserch',
            component: LineWidth
        }
    ]
})

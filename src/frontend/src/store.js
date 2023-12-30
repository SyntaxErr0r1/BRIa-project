import { createStore } from 'vuex'
import axios from 'axios'

const protocol = 'http'
const port = 8888
const hostname = 'localhost'
// const host = `${protocol}://${hostname}:${port}`
const host = '/api'

axios.defaults.baseURL = `${location.origin}/api`

const store = createStore({
    state () {
        return {
            recordings: [],
        }
    },
    mutations: {
        async loadRecordings (state, recordings) {
            state.recordings = await axios.get(`/recordings/`).then(response => response.data)
        }
    },
    actions: {
        loadRecordings (context) {
            context.commit('loadRecordings')
        }
    }
})

export default store
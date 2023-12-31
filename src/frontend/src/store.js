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
        async loadRecordings (context) {
            context.commit('loadRecordings')
        },
        async deleteRecording (context, recording) {
            await axios.delete(`/recordings/${recording.id}`)
            context.commit('loadRecordings')
        },
        async uploadRecording (context, recording) {
            // res = await axios.post(`/recordings/`, recording, { headers: { 'Content-Type': 'multipart/form-data' } })
            // context.commit('loadRecordings')
            return new Promise((resolve, reject) => {
                axios.post(`/recordings/`, recording, { headers: { 'Content-Type': 'multipart/form-data' } })
                    .then(response => {
                        context.commit('loadRecordings')
                        resolve(response)
                    })
                    .catch(error => {
                        reject(error)
                    })
            })
        },
    }
})

export default store
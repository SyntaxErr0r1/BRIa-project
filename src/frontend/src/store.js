import { createStore } from 'vuex'
import axios from 'axios'
import { useToast } from 'primevue/usetoast';

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
            modules: [],
        }
    },
    mutations: {
        async loadRecordings (state) {
            state.recordings = await axios.get(`/recordings/`).then(response => response.data)
        },
        async loadModules (state) {
            state.modules = await axios.get(`/modules/`).then(response => response.data).catch(error => console.log(error))
        },
    },
    actions: {
        async loadRecordings (context) {
            context.commit('loadRecordings')
        },
        async deleteRecording (context, id) {
            await axios.delete(`/recordings/${id}`)
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
        async loadModules (context) {
            context.commit('loadModules')
        },

        async updateModule (context, module) {
            await axios.post(`/modules/${module.id}/`, module)
            context.commit('loadModules')
        },

        async processModule (context, module) {
            return new Promise((resolve, reject) => {
                axios.post(`/modules/${module.id}/process/`, module)
                    .then(response => {
                        context.commit('loadModules')
                        resolve(response)
                    })
                    .catch(error => {
                        reject(error)
                    })
            })
        }
        
    }
})

export default store
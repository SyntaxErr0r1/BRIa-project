<template>
    <div>
        <h1>Upload Data</h1>

            <div class="input-item">
                <label for="name">Recording Name</label>
                <InputText id="name" v-model="name" aria-describedby="name-help" minlength="1" :class="{ 'p-invalid': errorMessage }"/>
            </div>

            <div class="input-item">
                <label for="dataset">Dataset File</label>
                <FileUpload id="dataset" mode="basic" name="dataset" :multiple="false" accept=".mat" customUpload @select="onSelect" :class="{ 'p-invalid': errorMessage }"></FileUpload>
            </div>

            <div class="input-item">
                <label for="description">Description</label>
                <InputText id="description" v-model="description" aria-describedby="description-help" :class="{ 'p-invalid': errorMessage }"/>
            </div>

            <div class="input-item">
                <label for="channels">Channels</label>
                <InputText id="channels" v-model="channelsStr" aria-describedby="channels-help" :class="{ 'p-invalid': errorMessage }"/>
            </div>

            <div class="input-item">
                <label for="datakey">Data Key</label>
                <InputText id="datakey" v-model="dataKey" aria-describedby="datakey-help" :class="{ 'p-invalid': errorMessage }"/>
                <small id="datakey-help" class="p-d-block">The key in the dataset file that contains the data.</small>
            </div>

            <div class="input-item">
                <label for="sampling_rate">Sampling Rate</label>
                <InputNumber 
                    id="sampling_rate" 
                    v-model="sampling_rate" 
                    aria-describedby="sampling_rate-help"
                    suffix="Hz"
                    :min="0"
                    :class="{ 'p-invalid': errorMessage }"
                />
            </div>

            <Button label="Upload" icon="pi" class="p-mr-2" @click="onSubmit" :loading="uploading"/>

            <!-- <small v-if="uploading" class="p-mt-2 p-warn">
                Data is uploading. Please wait.
            </small> -->

            <div v-if="errorMessage" class="p-mt-2 p-error error-message">
                {{ errorMessage }}
            </div>  
    </div>

</template>
<script>
import FileUpload from 'primevue/fileupload';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Button from 'primevue/button';
import ProgressBar from 'primevue/progressbar';

import { useToast } from "primevue/usetoast";

export default {
    components: {
        FileUpload,
        InputText,
        InputNumber,
        Button,
        ProgressBar,

    },
    name: 'UploadData',
    data: () => {
        return {
            dataset: null,
            name: "",
            description: "",
            sampling_rate: 0,
            channelsStr: "",
            errorMessage: null,
            dataKey: "",
            uploading: false,
            toast: useToast(),
        }
    },
    methods: {
        onSelect: function (event) {
            console.log(event);
            if(!event.files) return;
            this.dataset = event.files[0];
            console.log(this.dataset);
        },
        validate: function() {
            if (!this.name) {
                this.errorMessage = "Please enter a name for the recording.";
                return false;
            }
            if (!this.dataset) {
                this.errorMessage = "Please select a dataset file (.mat).";
                return false;
            }
            if (!this.sampling_rate) {
                this.errorMessage = "Please enter a sampling rate.";
                return false;
            }

            const pattern = /^[A-Za-z0-9]+(?:,[A-Za-z0-9]+)*$/;

            if (!pattern.test(this.channelsStr)) {
                this.errorMessage = "Please enter a list of channels separated by commas.";
                return false;
            }
             
            this.errorMessage = null;
            return true;
        },

        onSubmit: async function() {
            if (!this.validate()) return;
            console.log("submitting");

            this.uploading = true;
            let toastUploading = this.toast.add({ severity: 'info', summary: 'Uploading Recording', detail: 'Your dataset is currently uploading. \n This may take a few minutes.\n Please wait.'});

            let formData = new FormData();

            formData.append('name', this.name);
            formData.append('description', this.description);
            formData.append('sampling_rate', this.sampling_rate);
            formData.append('file', this.dataset);
            formData.append('channels', this.channelsStr);
            formData.append('data_key', this.dataKey);
            formData.append('date', new Date());


            this.$store.dispatch('uploadRecording', formData)
            .then((response) => {
                // this.$router.push({ name: 'LoadData' });
                console.log("success", response);
                this.toast.add({ severity: 'success', summary: 'Upload Successful', detail: 'Your dataset has been uploaded successfully.', life: 5000});
                
                if (response.data && response.data.warning)
                    this.toast.add({ severity: 'warn', summary: 'Upload Successful', detail: response.data.warning, life: 5000});
            })
            .catch((error) => {
                console.log("error",error);
                this.toast.add({ severity: 'error', summary: 'Upload Failed', detail: 'Your dataset failed to upload.', life: 5000});
                this.errorMessage = error.response.data.message;
            }).finally(() => {
                this.uploading = false;
                this.toast.remove(toastUploading);
            });
        },
        
    },

    // mounted: function() {
    //     console.log("mounted");
    //     let toastUploading = this.toast.add({ severity: 'info', summary: 'Uploading Recording', detail: 'Your dataset is currently uploading. \n This may take a few minutes.\n Please wait.'});
    //     // wait 2 seconds and then remove the toast
    //     setTimeout(() => {
    //         this.toast.remove(toastUploading);
    //     }, 2000);
    // },
}
</script>
<style lang="scss">

.input-item {
    margin-bottom: 1rem;
}
.input-item > * {
    display: block;
    margin-bottom: 0.5rem;
}
.error-message {
    margin-top: 0.5rem;
}
    
</style>
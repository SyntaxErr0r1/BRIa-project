<template>
    <div>
        <h1>Load Dataset</h1>

        <div class="p-fluid p-formgrid p-grid">
            
            <!-- <div class="p-field p-col-12 p-md-6">
                <label for="dataset">Dataset</label>
                <InputText id="dataset" v-model="dataset" />
            </div> -->

            <label for="dataID" value="Data ID" >Dataset Selection</label>
            <Dropdown v-model="selectedRecording" :options="recordings" filter optionLabel="name" placeholder="Select a Dataset" class="w-full md:w-14rem">
                <template #value="slotProps">
                    <div v-if="slotProps.value" class="flex align-items-center">
                        <div> ID:{{slotProps.value.id}} - <strong>{{ slotProps.value.name }} </strong></div>
                    </div>
                    <span v-else>
                        {{ slotProps.placeholder }}
                    </span>
                </template>
                <template #option="slotProps">
                    <div class="flex align-items-center">
                        <!-- <img :alt="slotProps.option.label" src="https://primefaces.org/cdn/primevue/images/flag/flag_placeholder.png" :class="`mr-2 flag flag-${slotProps.option.code.toLowerCase()}`" style="width: 18px" /> -->
                        <div> ID:{{slotProps.option.id}} - <strong>{{ slotProps.option.name }} </strong></div>
                    </div>
                </template>
            </Dropdown>


            <br>

            <label for="montageID" value="Montage ID" >Montage ID</label>
            <InputText id="montageID" v-model="loadDataModule.montageId" placeholder="Montage ID" class="w-full md:w-14rem" />

            &nbsp;

            <Button label="Confirm" icon="pi pi-check"  @click="confirm" />

            <h2>
                Data plot of Recording ID: {{loadDataModule.dataId}}
            </h2>

            <div class="figure">
                <!-- <ProgressSpinner  /> -->
                <ProgressSpinner class="progress-spinner" strokeWidth="8" fill="var(--surface-ground)"
        animationDuration="1s" aria-label="Custom ProgressSpinner" v-if="loadDataModule.statusProcessing" />
                <img :src="'/api'+loadDataModule.plotUrl" alt="">
            </div>
        </div>
    </div>
</template>
<script>
import ProgressSpinner from 'primevue/progressspinner';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Button from 'primevue/button';
import { useToast } from 'primevue/usetoast';
export default {

    components: {
        InputText,
        Dropdown,
        Button,
        ProgressSpinner,
    },

    name: 'LoadData',

    computed: {
        loadDataModule: function() {
            if (this.$store.state.modules.length >= 1) {
                return this.$store.state.modules[0];
            }else{
                return {};
            }
        },
        recordings: function() {
            return this.$store.state.recordings;
        }
    },

    data: () => {
        return {
            selectedRecording: null,
            toast: useToast(),
        }
    },
    
    mounted: function() {
        this.$store.dispatch('loadRecordings');
        this.$store.dispatch('loadModules');
    },

    methods: {
        confirm: function() {
            
            if(this.selectedRecording)
                this.$store.state.modules[0].dataId = this.selectedRecording.id;
            else{
                this.toast.add({severity:'error', summary: 'Error', detail: 'Please select a dataset', life: 3000});
                return;
            }
            
            this.$store.dispatch('updateModule', this.loadDataModule);
            this.$store.dispatch('processModule', this.loadDataModule);
        }
    }
}
</script>
<style lang="scss">
    .figure {
        position: relative;
        // width: 100%;
        // height: 100%;
    }
    .progress-spinner {
        height: 10rem;
        width: 10rem;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%); 
        position: absolute;
        margin: 0 auto;
        display: block;
    }
</style>
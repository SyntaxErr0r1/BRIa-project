<template lang="">

    <h2>Filter settings</h2>
    <div class="input-field">
        <label for="cutoff">Cut Off Frequency</label>
        <InputNumber id="cutoff" v-model="highPassModule.cutOff" placeholder="Cut off fequency" suffix="Hz"/>
    </div>
    
    <h2>Figure</h2>
    <Figure :src="'/api'+highPassModule.plotUrl" :loading="highPassModule.statusProcessing" :disabled="!hasModule" />

    <Button @click="confirm">Confirm</Button>
</template>
<script>
import InputNumber from 'primevue/inputnumber';
import Button from 'primevue/button';
import ProgressSpinner from 'primevue/progressspinner';
import Figure from '../components/Figure.vue';
import { useToast } from 'primevue/usetoast';

export default {
    components: {
        InputNumber,
        Button,
        ProgressSpinner,
        Figure,
    },
    name: 'HighPassFilter',
    data: () => {
        return {
            toast: useToast(),
        }
    },
    methods: {
        confirm: function() {
            this.$store.dispatch('updateModule', this.highPassModule)
            this.$store.dispatch('processModule', this.highPassModule).then(() => {
                this.toast.add({severity:'success', summary: 'Success', detail: 'High pass filter applied', life: 3000});
            }).catch((error) => {
                this.toast.add({severity:'error', summary: 'Error processing the module', detail: error, life: 3000});
            });
        }
    },
    computed: {
        highPassModule: function() {
            if (this.$store.state.modules.length >= 3) {
                return this.$store.state.modules[1];
            }else{
                return {};
            }
        },
        hasModule: function() {
            return this.highPassModule && this.highPassModule.id;
        }
    },
    mounted: function() {
        this.$store.dispatch('loadModules');
    }
}
</script>
<style lang="scss">
    
    .input-field > * {
        display: block;
    }
</style>
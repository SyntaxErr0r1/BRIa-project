<template lang="">

    <h2>Filter settings</h2>
    <div class="input-field">
        <label for="cutoff">Cut Off Frequency</label>
        <InputNumber id="cutoff" v-model="highPassModule.cutOff" placeholder="Cut off fequency" suffix="Hz"/>
    </div>
    
    <h2>Figure</h2>
    <Figure :src="'/api'+highPassModule.plotUrl" :loading="highPassModule.statusProcessing" />

    <Button @click="confirm">Confirm</Button>
</template>
<script>
import InputNumber from 'primevue/inputnumber';
import Button from 'primevue/button';
import ProgressSpinner from 'primevue/progressspinner';
import Figure from '../components/Figure.vue';

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
            
        }
    },
    methods: {
        confirm: function() {
            this.$store.dispatch('updateModule', this.highPassModule);
            this.$store.dispatch('processModule', this.highPassModule);
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
    },
}
</script>
<style lang="scss">
    
    .input-field > * {
        display: block;
    }
</style>
<template lang="">
    <h1>
        Independent Component Analysis
    </h1>

    <h2>
        Topographic Maps of Independent Components
    </h2>
    <Figure :src="'/api'+icaModule.componentsPlotUrl" :loading="icaModule.statusProcessing" />

    <h2>
        Removed Components
    </h2>
    <InputText v-model="icaModule.removedComponents" placeholder="eg. 0,1,2,9,10,17"/>
    <br>

    <h2>
        Figure
    </h2>
    <Figure :src="'/api'+icaModule.plotUrl" :loading="icaModule.statusProcessing" />

    <Button @click="confirm">Confirm</Button>
</template>
<script>
import Figure from '../components/Figure.vue';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
export default {
    name: 'ICA',
    components: {
        Figure,
        Button,
        InputText,
    },
    data: () => {
        return {
            
        }
    },
    methods: {
        confirm: function() {
            this.$store.dispatch('updateModule', this.icaModule);
            this.$store.dispatch('processModule', this.icaModule);
        }
    },
    computed: {
        icaModule: function() {
            console.log(this.$store.state.modules);
            if (this.$store.state.modules.length >= 3) {
                return this.$store.state.modules[2];
            }else{
                return {};
            }
        },
    },
    mounted: function() {
        this.$store.dispatch('loadModules');
    }
}
</script>
<style lang="scss">
    
</style>
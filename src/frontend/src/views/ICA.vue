<template lang="">
    <h1>
        Independent Component Analysis
    </h1>

    <h2>
        Topographic Maps of Independent Components
    </h2>
    <Figure :src="'/api'+icaModule.componentsPlotUrl" :loading="icaModule.statusProcessing" />

    <br>

    <Button @click="confirm">Confirm</Button>
</template>
<script>
import Figure from '../components/Figure.vue';
import Button from 'primevue/button';
export default {
    name: 'ICA',
    components: {
        Figure,
        Button,
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
            if (this.$store.state.modules.length >= 2) {
                return this.$store.state.modules[2];
            }else{
                return {};
            }
        },
    },
}
</script>
<style lang="scss">
    
</style>
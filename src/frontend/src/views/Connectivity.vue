<template lang="">
    <div>
        <h1>Connectivity Analysis</h1>   

        <h2>Connectivity Analysis</h2>
        <Figure :src="'/api'+connectivityModule?.plotConnectivity" :loading="connectivityModule?.statusProcessing" :disabled="!connectivityModule" />

        <h2>Connectivity Matrix</h2>

        <!-- <h2>Connectivity Matrix</h2> -->
        <Button @click="confirm">Confirm</Button>
    </div>
</template>
<script>
import Figure from '@/components/Figure.vue';
import Button from 'primevue/button';

export default {
    name: 'Connectivity',
    data: () => {
        return {
            
        }
    },
    components: {
        Figure,
        Button
    },
    methods: {
        confirm: function() {
            this.$store.dispatch('updateModule', this.connectivityModule);
            this.$store.dispatch('processModule', this.connectivityModule);
        }
    },
    computed: {
        connectivityModule: function() {
            return this.$store.state.modules[3];
        }
    }, 
    mounted: function() {
        this.$store.dispatch('loadModules');
    }
}
</script>
<style lang="">
    
</style>
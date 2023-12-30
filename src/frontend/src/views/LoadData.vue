<template>
    <div>
        <h1>Load Dataset</h1>

        <div class="p-fluid p-formgrid p-grid">
            
            <!-- <div class="p-field p-col-12 p-md-6">
                <label for="dataset">Dataset</label>
                <InputText id="dataset" v-model="dataset" />
            </div> -->

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

        </div>
    </div>
</template>
<script>
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
export default {
    components: {
        InputText,
        Dropdown
    },
    name: 'LoadData',
    data: () => {
        return {
            selectedRecording: null
        }
    },
    computed: {
        recordings: function() {
            return this.$store.state.recordings;
        }
    },
    mounted: function() {
        this.$store.dispatch('loadRecordings');
    },
}
</script>
<style lang="scss">
    
</style>
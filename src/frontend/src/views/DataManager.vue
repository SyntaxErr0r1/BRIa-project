<template lang="">
    <div>
        <DataTable :value="recordings" tableStyle="min-width: 50rem">
            <Column field="id" header="ID"></Column>
            <Column field="name" header="Name"></Column>
            <Column field="description" header="Description"></Column>
            <Column field="created_at" header="Created At"></Column>
            <Column field="sampling_rate" header="Sampling rate"></Column>
            <Column field="action" header="Action">
                <template #body="slotProps">
                    <!-- <Button icon="pi pi-play" class="p-button-rounded p-button-success p-mr-2" /> -->
                    <Button icon="pi pi-trash" class="p-button p-button-danger" @click="deleteRecording(slotProps.rowData.id)" />
                </template>
            </Column>
        </DataTable>
    </div>
</template>
<script>

import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';   // optional
import Row from 'primevue/row';                   // optional
import Button from 'primevue/button';
import 'primeicons/primeicons.css'


export default {
    components: {
        DataTable,
        Column,
        ColumnGroup,
        Row,
        Button
    },
    name: 'DataManager',
    methods: {
        deleteRecording: function(id) {

            // this.$store.dispatch('deleteRecording', id);
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
<style lang="">
    
</style>
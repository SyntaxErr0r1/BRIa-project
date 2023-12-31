<template lang="">
    <div class="figure">
        <!-- <ProgressSpinner  /> -->
        <ProgressSpinner class="progress-spinner" strokeWidth="8" fill="var(--surface-ground)"
animationDuration="1s" aria-label="Custom ProgressSpinner" v-if="loading" />
        <img :src="src" alt="Figure">
    </div>
</template>
<script>
import ProgressSpinner from 'primevue/progressspinner';
export default {
    name: 'Figure',
    components: {
        ProgressSpinner,
    },
    props: {
        src: {
            required: true,
        },
        loading: {
            type: Boolean,
            default: false,
        },
    },
}
</script>
<style lang="scss">
    .figure {
        position: relative;
        width: 100%;
        height: auto;
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
<template lang="">
    <div class="figure">
        <!-- <ProgressSpinner  /> -->
        <ProgressSpinner class="progress-spinner" strokeWidth="8" fill="var(--surface-ground)"
animationDuration="1s" aria-label="Custom ProgressSpinner" v-if="loading" />
        <img :src="src+'?rnd='+cacheKey" alt="Figure" v-if="!disabled">
        <img src="../assets/placeholder.svg" alt="Figure Placehorder" v-if="disabled">
    </div>
</template>
<script>
import ProgressSpinner from 'primevue/progressspinner';
export default {
    name: 'Figure',
    components: {
        ProgressSpinner,
    },
    data: () => {
        return {
            cacheKey: +new Date(),
            interval: null,
        }
    },
    props: {
        src: {
            required: true,
        },
        loading: {
            type: Boolean,
            default: false,
        },
        disabled: {
            type: Boolean,
            default: false,
        },
    },

    created() {
        this.interval = setInterval(() => {
            this.cacheKey = +new Date();
        }, 1000);
    },

    destroyed() {
        clearInterval(this.interval);
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
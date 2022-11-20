<script>
    import Slider from '@smui/slider';
    import { Col, Container, Row } from 'sveltestrap';
    import 'bootstrap/dist/css/bootstrap.min.css';
    import { createEventDispatcher } from 'svelte';
	import Range from "./Range.svelte";

    export let name = "unnamed";
    export let value = 0; // 0.0 - 1.0
    export let type; // e.g. "years"
    let level;
    $: {
        if(name === "Years in Future to Predict") {
            level = value;
        } else if(value <= 6) {
            level = "low importance";
        } else if(value <= 14) {
            level = "medium importance";
        } else {
            level = "high importance";
        }
    }


    const dispatch = createEventDispatcher()
    function triggerUpdate() {
        console.log("dispatched");
        dispatch('trigger');
    }
</script>

<div class="p-8 bg-amber-300">
    <Container fluid>
        <div class="row align-items-center justify-content-center">
            <div class="col-sm-12 col-md-8"> 
                <Row>
                    <div class="col-sm-12 col-md-4 text-end">
                        <pre class="col status">{name}: </pre>
                    </div>
                    <div class="col-sm-12 col-md-4">
                        <!--<Slider class="col" style="flex-grow: 1;" bind:value min={0} max={10} step={1} on:change={() => triggerUpdate()} />-->
                        <Range on:changedrag={(e) => {value = e.detail.value; triggerUpdate();}} id="basic-slider" />
                    </div>
                    <div class="col-sm-12 col-md-4 text-start">
                        <pre class="col status">{level}</pre>
                    </div>
                </Row>
            </div>
            
        </div>
        
    </Container>
</div>
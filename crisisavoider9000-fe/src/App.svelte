<script>
    import Gewichtung from "./Gewichtung.svelte";

    let selCity = true;
    let url_pos = selCity ? "City" : "State";

    let city_header = ["Score", "City", "State", "Buy-out (Years)", "Housing Lifetime (Years)", "Environmental Risk (%)", "Increase in Value (%)"]
    let state_header = ["Score", "State", "Buy-out (Years)", "Housing Lifetime (Years)", "Environmental Risk (%)", "Increase in Value (%)"]
    let header = selCity ? city_header : state_header;

    let buyout_weight = 10;
    let housing_lifetime_weight = 10;
    let environmental_risk_weight = 10;
    let price_development_weight = 10;
    let time_slide_value = 10;

    export async function updateData() {
      const res = await fetch(`http://127.0.0.1:8000/v1/${url_pos.toLowerCase()}?buyout_weight=${buyout_weight}&housing_lifetime_weight=${housing_lifetime_weight}&environmental_risk_weight=${environmental_risk_weight}&price_development_weight=${price_development_weight}&time_slide_value=${time_slide_value}`, {
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          }
        });
      let text = await res.json();
      
      if (res.ok) {
        return text;
      } else {
        throw new Error(text);
      }
    }

    let promise = updateData();
    function handleUpdate() {
      promise = updateData();
    }

    function toggleCity() {
      selCity = !selCity;
      url_pos = selCity ? "City" : "State";
      header = selCity ? city_header : state_header;
      handleUpdate();
    }

    function roundNumber(number) {
      if(isNaN(number)){
        return number;
      }
      return Number(number).toFixed(2);
    }

</script>

	
<h1 class="text-3xl font-bold underline">
  CrisisAvoider9000 💥🚀
</h1>
<br>

<div>
  <Gewichtung name="Quick Buy-out" bind:value={buyout_weight} type="years" on:trigger={handleUpdate}/>
  <Gewichtung name="Long Housing Lifetime" value={housing_lifetime_weight}  type="years" on:trigger={handleUpdate} />
  <Gewichtung name="Low Environmental Risks" value={environmental_risk_weight}  type="years" on:trigger={handleUpdate} />
  <Gewichtung name="Increase in Value" value={price_development_weight}  type="years" on:trigger={handleUpdate} />
  <Gewichtung name="Years in Future to Predict" value={time_slide_value}  type="years" on:trigger={handleUpdate} />
  <p>Choose your location granularity:</p>
  <button on:click={toggleCity}>{url_pos}</button>
</div>

<br>


<div>

  {#await promise}
    <p>...waiting</p>
  {:then data}
    

    <table class="blueTable">
      <thead>
        <tr>
          {#each header as columnHeading}
            <th>{columnHeading}</th>
          {/each}
        <tr/>
      </thead>
      <tbody>
        {#each Object.values(data) as row}
          <tr>
            {#each Object.values(row) as cell, i}
            {#if selCity && (i == 5 || i == 6) || !selCity && (i == 4 || i == 5) }
              <td>{roundNumber(cell*100)}</td>
            {:else}
              <td>{roundNumber(cell)}</td>
            {/if}
            {/each}
          </tr>
        {/each}
      </tbody>
    </table>

  {:catch error}
    <p>An error occurred!</p>
    <p>{error}</p>
  {/await}

  
</div>

<style>
	table, th, td {
		border: 1px solid;
		border-collapse: collapse;
		margin-bottom: 10px;
	}

	table.redTable thead th {
		font-size: 19px;
		font-weight: bold;
		color: #FFFFFF;
		text-align: center;
		border-left: 2px solid #A40808;
	}
	table.redTable thead th:first-child {
		border-left: none;
	}

		table.blueTable {
		border: 1px solid #1C6EA4;
		background-color: #EEEEEE;
		width: 100%;
		text-align: left;
		border-collapse: collapse;
	}
	table.blueTable td, table.blueTable th {
		border: 1px solid #AAAAAA;
		padding: 3px 2px;
	}
	table.blueTable tbody td {
		font-size: 13px;
	}
	table.blueTable tr:nth-child(even) {
		background: #D0E4F5;
	}
	table.blueTable thead {
		background: #1C6EA4;
		background: -moz-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
		background: -webkit-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
		background: linear-gradient(to bottom, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
		border-bottom: 2px solid #444444;
	}
	table.blueTable thead th {
		font-size: 15px;
		font-weight: bold;
		color: #FFFFFF;
		border-left: 2px solid #D0E4F5;
	}
	table.blueTable thead th:first-child {
		border-left: none;
	}
</style>
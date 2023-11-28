<template>
  <div>
    <div class="grid">
    <ul>
      <li v-for="key in Object.keys(result)">{{ key }}: {{ (result as any)[key].map }}</li>
    </ul>
    <ul>
      <li v-for="key in Object.keys(result)">{{ key }}: {{ (result as any)[key].precision[10] }}</li>
    </ul>
    </div>
    <div class="grid">
      <div style="height: 350px" v-for="data in chartData">
        <LineChart
          :chartData="generateChartData(data.query)"
          :title="data.title"
        />
      </div>
    </div>
    <div class="grid">
      <div style="height: 350px" v-for="data in chartData">
        <BarChart
          :chartData="generateBarChartData(data.query)"
          :title="data.title"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import LineChart from "./components/LineChart.vue";
import BarChart from "./components/BarChart.vue";
import result from "./assets/data/query.json";

const chartData = [
  {
    title: "Raw string without stemming",
    query: (catagory: string) =>
      catagory.includes("raw-noStemming") && !catagory.includes("441-450"),
  },
  {
    title: "Raw string with Porter stemming",
    query: (catagory: string) =>
      catagory.includes("raw-porterStemming") && !catagory.includes("441-450"),
  },
  {
    title: "Trec web without stemming",
    query: (catagory: string) =>
      catagory.includes("trec-noStemming") && !catagory.includes("441-450"),
  },
  {
    title: "Trec web with Porter stemming",
    query: (catagory: string) =>
      catagory.includes("trec-porterStemming") && !catagory.includes("441-450"),
  },
  {
    title: "Raw string without stemming",
    query: (catagory: string) =>
      catagory.includes("raw-noStemming") && catagory.includes("441-450"),
  },
  {
    title: "Raw string with Porter stemming",
    query: (catagory: string) =>
      catagory.includes("raw-porterStemming") && catagory.includes("441-450"),
  },
  {
    title: "Trec web without stemming",
    query: (catagory: string) =>
      catagory.includes("trec-noStemming") && catagory.includes("441-450"),
  },
  {
    title: "Trec web with Porter stemming",
    query: (catagory: string) =>
      catagory.includes("trec-porterStemming") && catagory.includes("441-450"),
  },
];

const generateChartData = (filter: (catagory: string) => boolean) => {
  return {
    labels: Array.from({ length: 10 }, (_, i) => (i + 1) / 10),
    datasets: Object.keys(result)
      .filter(filter)
      .map((key: string) => {
        const color = () => {
          switch (key.split("-").slice(2)[0]) {
            case "bm25":
              return "#3498DB";
            case "laplace":
              return "#2ECC71";
            case "jm":
              return "#FFA500";
            case "LTR":
              return "#FF5733";
          }
        };
        return {
          label: key.split("-").slice(2)[0],
          borderColor: color,
          backgroundColor: color,
          data: Object.values((result as any)[key].ap) as number[],
        };
      }),
  };
};

const generateBarChartData = (filter: (catagory: string) => boolean) => {
  return {
    labels: Object.keys(result)
      .filter(filter)
      .map((key: string) => key.split("-").slice(2)[0]),
    datasets: [
      // {
      //   label: "retrieved",
      //   backgroundColor: "#3498DB",
      //   data: Object.keys(result)
      //     .filter(filter)
      //     .map((key: string) => (result as any)[key].stats.retrieved - (result as any)[key].stats.rel_ret),
      // },
      {
        label: "rel_ret",
        backgroundColor: "rgba(46, 204, 113, 0.2)",
        borderColor: "rgb(46, 204, 113)",
        borderWidth: 1,
        data: Object.keys(result)
          .filter(filter)
          .map((key: string) => (result as any)[key].stats.rel_ret),
      },
      {
        label: "retrieved",
        backgroundColor: "rgba(255, 165, 0, 0.2)",
        borderColor: "rgba(255, 165, 0, 1)",
        borderWidth: 1,
        data: Object.keys(result)
          .filter(filter)
          .map((key: string) => (result as any)[key].stats.relevant - (result as any)[key].stats.rel_ret),
      },
    ],
  };
};
</script>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}
</style>

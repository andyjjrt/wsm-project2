<template>
  <Line id="my-chart-id" :options="chartOptions" :data="chartData" />
</template>

<script setup lang="ts">
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartData,
} from "chart.js";
import { Line } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const props = defineProps<{
  chartData: ChartData<"line", number[], unknown>;
  title: string;
}>();

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      max: 1,
      min: 0,
      ticks: {
        stepSize: 0.05,
      },
    },
  },
  plugins: {
    title: {
      display: true,
      text: props.title,
      font: {
        size: 22,
      },
    },
  },
  // plugins: {
  //   tooltip: {
  //     callbacks: {
  //       label: (tooltipItems: any) => {
  //         let stats = tooltipItems.dataset.data;
  //         let total = 0;
  //         for (let i in stats) {
  //           total += stats[i];
  //         }
  //         return ` ${tooltipItems.raw} (${(
  //           (tooltipItems.raw * 100) /
  //           total
  //         ).toFixed(2)}%)`;
  //       },
  //     },
  //   },
  // },
};
</script>

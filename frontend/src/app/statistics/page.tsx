"use client";
import { Graph } from "@/components/Graph";
import { useBackend } from "@/services/backend";
import { DerangedStatistic } from "@/types/rest";
import { CircularProgress, Stack, Typography } from "@mui/material";

// const testFetcher = () =>
//     Promise.resolve({
//         "Average plant conditions by days": [
//             ["2025-01-13", 1001.4, 22.62, 22.1],
//             ["2025-01-14", 1000.61, 22.62, 22.24],
//         ],
//     });
export default function Page() {
    const plantation = "1735683658.5245671485665a807c7-5986-4338-920e-7eba0cfd9528";
    const { data: dataPayload, isLoading } = useBackend<DerangedStatistic>("/api/statistics", {
        plantationUUID: plantation as string,
    });
    const data = dataPayload?.["Average plant conditions by days"];
    if (!data && !isLoading) {
        return "error";
    }
    if (isLoading) {
        return <CircularProgress />;
    }

    const xAxis = data!.map((entry) => entry[0]);
    const temperature = data!.map((entry) => entry[1]);
    const moisture = data!.map((entry) => entry[2]);
    const illuminance = data!.map((entry) => entry[3]);

    return (
        <Stack gap={3}>
            <Typography variant="h5" component="h2">
                Statystyki
            </Typography>
            <Graph color="#ce0606" data={temperature} label="Temperatura" xAxis={xAxis} />
            <Graph color="#02d5d1" data={moisture} label="Wilgotność gleby" xAxis={xAxis} />
            <Graph color="#f28e2c" data={illuminance} label="Nasłonecznienie" xAxis={xAxis} />
            {/* <Paper sx={{ p: 2 }}>
                <Typography variant="h6">Zużycie wody</Typography>
                <LineChart
                    series={[{ label: "zużycie wody", area: true, data: [1, 2, 3, 2, 1, 0.4] }]}
                    height={300}
                    slotProps={{
                        legend: {
                            position: { vertical: "bottom", horizontal: "middle" },
                        },
                    }}
                />
            </Paper>
            <Paper sx={{ p: 2 }}>
                <Typography variant="h6">Naświetlenie</Typography>
                <LineChart
                    height={300}
                    series={[
                        {
                            label: "naświetlenie",
                            area: true,
                            color: "#f28e2c",
                            data: [1, 2, 3, 2, 1, 0.4],
                        },
                    ]}
                    slotProps={{
                        legend: {
                            position: { vertical: "bottom", horizontal: "middle" },
                        },
                    }}
                />
            </Paper> */}
        </Stack>
    );
}

import { Paper, Stack, Typography } from "@mui/material";
import { LineChart } from "@mui/x-charts";

export default function Page() {
    return (
        <Stack gap={3}>
            <Typography variant="h5" component="h2">
                Statystyki
            </Typography>
            <Paper sx={{ p: 2 }}>
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
            </Paper>
        </Stack>
    );
}

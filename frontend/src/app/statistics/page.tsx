import { FormControl, InputLabel, MenuItem, Select, Stack, Typography, Paper } from "@mui/material";
import { LineChart } from "@mui/x-charts";

export default function Page() {
    return (
        <Stack gap={3}>
            <Typography variant="h5" component="h2">
                Statystyki
            </Typography>
            <FormControl>
                <InputLabel id="fruit-picker-label">Roślina</InputLabel>
                <Select
                    labelId="fruit-picker-label"
                    id="fruit-picker"
                    // value={selectedFruit}
                    // onChange={handleFruitChange}
                >
                    <MenuItem value="borowka">Borówka amerykańska</MenuItem>
                    <MenuItem value="truskawka">Truskawka</MenuItem>
                </Select>
            </FormControl>
            <Paper sx={{ p: 2 }}>
                <Typography variant="h6">Wilgotność</Typography>
                <LineChart
                    xAxis={[{ data: [5,6,7,8,9,10] }]}
                    series={[{ label: "wilgotność", area: true, data: [345, 345, 363, 250, 100, 80] }]}
                    height={300}
                    slotProps={{
                        legend: {
                            position: { vertical: "bottom", horizontal: "middle" },
                        },
                    }}
                />
            </Paper>
            <Paper sx={{ p: 2 }}>
                <Typography variant="h6">Temperatura</Typography>
                <LineChart
                    series={[{ label: "temperatura", area: true, color: "red", data: [20, 22.4, 23, 23.2, 24, 24.4] }]}
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

"use client";
import { Paper, Stack, Typography } from "@mui/material";
import useSWR from "swr";
import { jsonFetcher, postBackend } from "@/services/backend";

import { DateCalendar } from '@mui/x-date-pickers/DateCalendar';
import { DayCalendarSkeleton } from '@mui/x-date-pickers/DayCalendarSkeleton';

export default function Page() {
    const { data: predictionRes, isLoading, mutate } = useSWR("/api/prediction", jsonFetcher);
    const prediction = predictionRes?.prediction;
    console.log(predictionRes)
    console.log(prediction)
    return (
        <Stack gap={3}>
            <Typography variant="h5" component="h2">
                Predykcje
            </Typography>
            <Paper sx={{ p: 2 }}>
                <Typography variant="h6">Borówka amerykańska</Typography>
                <Typography>Następne podlewanie - 17.01.2025</Typography>
            </Paper>
            <Paper sx={{ p: 2 }}>
            <Typography variant="h6">Truskawka</Typography>
                <Typography>Następne podlewanie - dzisiaj!</Typography>
            </Paper>
            <DateCalendar
                loading={isLoading}
                renderLoading={() => <DayCalendarSkeleton />}
                // slots={{
                //     day: ,
                // }}
                // slotProps={{
                //     day: {
                //     highlightedDays,
                //     } as any,
                // }}
            />
        </Stack>
    );
}

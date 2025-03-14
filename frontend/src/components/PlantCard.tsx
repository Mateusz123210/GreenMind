"use client";
import {
    Box,
    BoxProps,
    Card,
    CardActionArea,
    CardContent,
    Collapse,
    LinearProgress,
    Stack,
    styled,
    Typography,
} from "@mui/material";
import { useMemo, useState } from "react";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { PlantSlider } from "./PlantSlider";
import { PlantConfig } from "@/types/rest";
import { deleteBackend, mapValue, putBackend, useBackend } from "@/services/backend";
import { RemoveButton } from "./RemoveButton";
import { mutate as globalMutate } from "swr";

interface ExpandMoreProps extends BoxProps {
    expand: boolean;
}

const ExpandMore = styled((props: ExpandMoreProps) => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { expand, ...other } = props;
    return <Box {...other} />;
})(({ theme }) => ({
    width: 24,
    height: 24,
    transition: theme.transitions.create("transform", {
        duration: theme.transitions.duration.shortest,
    }),
    variants: [
        {
            props: ({ expand }) => !expand,
            style: {
                transform: "rotate(0deg)",
            },
        },
        {
            props: ({ expand }) => !!expand,
            style: {
                transform: "rotate(180deg)",
            },
        },
    ],
}));

type SliderType = "temperature" | "moisture" | "illuminance";

interface Props {
    title: string;
    id: string;
}
// const dupaFetcher = (...args: any) => Promise.resolve({
//     max_illuminance: 20,
//     comments: "sdfzsdf",
//     max_moisture: 10,
//     max_temperature: 10,
//     min_illuminance: 0,
//     min_moisture: 0,
//     min_temperature: 0,
//     name: "dupa",
//     opt_illuminance: 4,
//     opt_moisture: 4,
//     opt_temperature: 4
// } satisfies PlantConfig)
export const PlantCard: React.FC<Props> = ({ title, id }) => {
    const [expanded, setExpanded] = useState<boolean>(false);
    const plantQueryParams = useMemo(() => ({ plantUUID: id }), [id]);
    const {
        data: plantConfigPreparsed,
        isLoading,
        mutate,
    } = useBackend<PlantConfig>("/api/plant", plantQueryParams);
    const plantConfig: PlantConfig | undefined = plantConfigPreparsed && {
        ...plantConfigPreparsed,
        min_moisture: mapValue(plantConfigPreparsed.min_moisture, 300, 1300, 0, 100),
        opt_moisture: mapValue(plantConfigPreparsed.opt_moisture, 300, 1300, 0, 100),
        max_moisture: mapValue(plantConfigPreparsed.max_moisture, 300, 1300, 0, 100),
    };
    const onValueChange = (type: SliderType) => (newValue: [number, number, number]) => {
        const payload: Partial<Record<keyof PlantConfig | "plantUUID", number | string>> = {};
        switch (type) {
            case "illuminance":
                payload["min_illuminance"] = newValue[0];
                payload["opt_illuminance"] = newValue[1];
                payload["max_illuminance"] = newValue[2];
                break;
            case "moisture":
                payload["min_moisture"] = mapValue(newValue[0], 0, 100, 300, 1300);
                payload["opt_moisture"] = mapValue(newValue[1], 0, 100, 300, 1300);
                payload["max_moisture"] = mapValue(newValue[2], 0, 100, 300, 1300);
                break;
            case "temperature":
                payload["min_temperature"] = newValue[0];
                payload["opt_temperature"] = newValue[1];
                payload["max_temperature"] = newValue[2];
                break;
        }
        const merged = Object.assign(plantConfig!, payload);
        payload["plantUUID"] = id;
        mutate(
            putBackend("/api/plant", payload).then(() => merged),
            {
                optimisticData: merged,
            }
        );
    };
    return (
        <Card>
            <CardActionArea onClick={() => setExpanded((expanded) => !expanded)}>
                <CardContent>
                    <Stack direction="row" justifyContent="space-between">
                        <Typography gutterBottom variant="h5">
                            {title}
                        </Typography>
                        <ExpandMore
                            expand={expanded}
                            aria-expanded={expanded}
                            aria-label="show more"
                        >
                            <ExpandMoreIcon />
                        </ExpandMore>
                    </Stack>
                </CardContent>
            </CardActionArea>
            <Collapse in={expanded} timeout="auto" unmountOnExit>
                {isLoading || !plantConfig ? (
                    <LinearProgress />
                ) : (
                    <>
                        <RemoveButton
                            onSubmit={() => {
                                globalMutate(
                                    "/api/plants",
                                    deleteBackend("/api/plant", { plantUUID: id })
                                );
                            }}
                        />
                        <CardContent>
                            <Typography variant="h6">uwagi</Typography>
                            <Typography variant="body2" pb={4}>
                                {plantConfig.comments}
                            </Typography>
                            <PlantSlider
                                label="Temperatura"
                                unit="°C"
                                value={[
                                    plantConfig!.min_temperature,
                                    plantConfig!.opt_temperature,
                                    plantConfig!.max_temperature,
                                ]}
                                onValueChange={onValueChange("temperature")}
                                length={13}
                                mult={5}
                                max={60}
                            />
                            <PlantSlider
                                label="Wilgotność"
                                unit="%"
                                value={[
                                    plantConfig!.min_moisture,
                                    plantConfig!.opt_moisture,
                                    plantConfig!.max_moisture,
                                ]}
                                onValueChange={onValueChange("moisture")}
                                length={21}
                                mult={5}
                                max={100}
                            />
                            <PlantSlider
                                label="Nasłonecznienie"
                                unit="lm"
                                value={[
                                    plantConfig!.min_illuminance,
                                    plantConfig!.opt_illuminance,
                                    plantConfig!.max_illuminance,
                                ]}
                                onValueChange={onValueChange("illuminance")}
                                length={21}
                                mult={250}
                                max={5000}
                            />
                        </CardContent>
                    </>
                )}
            </Collapse>
        </Card>
    );
};

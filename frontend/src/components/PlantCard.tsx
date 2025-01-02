"use client";
import {
    Box,
    BoxProps,
    Card,
    CardActionArea,
    CardContent,
    Collapse,
    Stack,
    styled,
    Typography,
} from "@mui/material";
import { useState } from "react";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { PlantSlider } from "./PlantSlider";

interface ExpandMoreProps extends BoxProps {
    expand: boolean;
}

const ExpandMore = styled((props: ExpandMoreProps) => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { expand, ...other } = props;
    return <Box {...other} />;
})(({ theme }) => ({
    width:24,
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

interface Props {
    title: string;
    description: string;
}
export const PlantCard: React.FC<Props> = ({ title, description }) => {
    const [expanded, setExpanded] = useState<boolean>(false);
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
                <CardContent>
                    <Typography variant="h6">
                        uwagi
                    </Typography>
                    <Typography variant="body2" pb={4}>{description}</Typography>
                    <PlantSlider label="Temperatura" unit="°C"/>
                    <PlantSlider label="Wilgotność" unit="%"/>
                    <PlantSlider label="Nasłonecznienie" unit="lm"/>
                </CardContent>
            </Collapse>
        </Card>
    );
};

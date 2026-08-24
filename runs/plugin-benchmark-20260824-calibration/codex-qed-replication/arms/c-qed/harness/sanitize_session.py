#!/usr/bin/env python3

import json
import pathlib
import sys


def selected_session_meta(Payload):
	return {
		"session_id": Payload.get("id") or Payload.get("session_id"),
		"timestamp": Payload.get("timestamp"),
		"cwd": Payload.get("cwd"),
		"originator": Payload.get("originator"),
		"cli_version": Payload.get("cli_version"),
		"source": Payload.get("source"),
		"model_provider": Payload.get("model_provider"),
		"memory_mode": Payload.get("memory_mode"),
		"multi_agent_version": Payload.get("multi_agent_version"),
	}


def main():
	if len(sys.argv) != 3:
		raise SystemExit("usage: sanitize_session.py INPUT.jsonl OUTPUT.jsonl")

	InputPath = pathlib.Path(sys.argv[1])
	OutputPath = pathlib.Path(sys.argv[2])
	SelectedRows = []

	with InputPath.open("r", encoding="utf-8") as InputHandle:
		for Line in InputHandle:
			Row = json.loads(Line)
			RowType = Row.get("type")
			Payload = Row.get("payload", {})
			Base = {
				"timestamp": Row.get("timestamp"),
				"ordinal": Row.get("ordinal"),
			}

			if RowType == "session_meta":
				Base["type"] = "session_meta"
				Base["payload"] = selected_session_meta(Payload)
				SelectedRows.append(Base)
				continue

			if RowType == "response_item" and Payload.get("type") == "custom_tool_call":
				Base["type"] = "tool_call"
				Base["payload"] = {
					"call_id": Payload.get("call_id"),
					"name": Payload.get("name"),
					"input": Payload.get("input"),
				}
				SelectedRows.append(Base)
				continue

			if RowType == "response_item" and Payload.get("type") == "custom_tool_call_output":
				Base["type"] = "tool_call_output"
				Base["payload"] = {
					"call_id": Payload.get("call_id"),
					"output": Payload.get("output"),
				}
				SelectedRows.append(Base)
				continue

			if RowType == "event_msg" and Payload.get("type") == "token_count":
				Base["type"] = "token_count"
				Base["payload"] = {
					"info": Payload.get("info"),
					"rate_limits": Payload.get("rate_limits"),
				}
				SelectedRows.append(Base)
				continue

			if RowType == "event_msg" and Payload.get("type") == "task_complete":
				Base["type"] = "task_complete"
				Base["payload"] = {
					"turn_id": Payload.get("turn_id"),
					"last_agent_message": Payload.get("last_agent_message"),
					"started_at": Payload.get("started_at"),
					"completed_at": Payload.get("completed_at"),
					"duration_ms": Payload.get("duration_ms"),
					"time_to_first_token_ms": Payload.get("time_to_first_token_ms"),
				}
				SelectedRows.append(Base)

	with OutputPath.open("w", encoding="utf-8", newline="\n") as OutputHandle:
		for Row in SelectedRows:
			OutputHandle.write(json.dumps(Row, ensure_ascii=True, sort_keys=True))
			OutputHandle.write("\n")


if __name__ == "__main__":
	main()

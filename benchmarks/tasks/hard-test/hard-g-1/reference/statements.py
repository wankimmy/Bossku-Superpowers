"""Monthly account statements, built on top of sessions.compute_session_fee."""
import logging
from dataclasses import dataclass
from decimal import Decimal

import clock as clock_module
import money
import sessions as sessions_module
import validation

_LOGGER = logging.getLogger("garage.statements")


@dataclass(frozen=True)
class StatementLine:
    vehicle_id: str
    entry_time: object
    exit_time: object
    fee: Decimal


@dataclass(frozen=True)
class Statement:
    account_id: str
    generated_on: object
    line_count: int
    gross_total: Decimal
    discount_percent: int
    discount_amount: Decimal
    statement_fee: Decimal
    final_total: Decimal
    lines: tuple


def _discount_percent_for(gross_total):
    if gross_total >= Decimal("500"):
        return 15
    if gross_total >= Decimal("200"):
        return 10
    if gross_total >= Decimal("50"):
        return 5
    return 0


def build_statement(account_id, sessions, rate_card, is_member=False, clock=None):
    validation.require_nonempty_str("account_id", account_id)
    validation.require_list_or_tuple("sessions", sessions)
    validation.require_type("rate_card", rate_card, sessions_module.RateCard)
    validation.require_type("is_member", is_member, bool)
    for index, item in enumerate(sessions):
        validation.require_type(f"sessions[{index}]", item, sessions_module.SessionRecord)

    active_clock = clock if clock is not None else clock_module.SystemClock()
    generated_on = active_clock.now()

    lines = []
    gross_total = Decimal("0.00")
    for item in sessions:
        fee = sessions_module.compute_session_fee(rate_card, item)
        gross_total += fee
        lines.append(StatementLine(item.vehicle_id, item.entry_time, item.exit_time, fee))

    lines.sort(key=lambda line: (line.entry_time, line.vehicle_id))

    discount_percent = _discount_percent_for(gross_total)
    discount_amount = money.round_money(gross_total * discount_percent / Decimal(100))
    net_total = gross_total - discount_amount
    statement_fee = Decimal("0.00") if is_member else Decimal("5.00")
    final_total = net_total + statement_fee

    _LOGGER.info(
        f"statement account={account_id} sessions={len(sessions)} "
        f"total={money.format_money(final_total)}"
    )

    return Statement(
        account_id=account_id,
        generated_on=generated_on,
        line_count=len(lines),
        gross_total=gross_total,
        discount_percent=discount_percent,
        discount_amount=discount_amount,
        statement_fee=statement_fee,
        final_total=final_total,
        lines=tuple(lines),
    )
